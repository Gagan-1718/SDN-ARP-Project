from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, arp, ipv4
from ryu.lib.packet import ether_types


class ARPController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(ARPController, self).__init__(*args, **kwargs)
        self.mac_to_port = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Table-miss flow entry
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                         ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(
            ofproto.OFPIT_APPLY_ACTIONS, actions)]

        mod = parser.OFPFlowMod(datapath=datapath,
                               priority=priority,
                               match=match,
                               instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            return

        dst = eth.dst
        src = eth.src

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        # Learn MAC
        self.mac_to_port[dpid][src] = in_port

        # Handle ARP
        arp_pkt = pkt.get_protocol(arp.arp)
        if arp_pkt:
            self.logger.info(f"ARP Packet: {arp_pkt.src_ip} -> {arp_pkt.dst_ip}")
            return

        # Handle IP (BLOCK LOGIC)
        ip_pkt = pkt.get_protocol(ipv4.ipv4)
        if ip_pkt:
            src_ip = ip_pkt.src
            dst_ip = ip_pkt.dst

            # 🚫 BLOCK h1 → h2
            if src_ip == "10.0.0.1" and dst_ip == "10.0.0.2":
                self.logger.info("BLOCKED TRAFFIC: h1 → h2")

                match = parser.OFPMatch(eth_type=0x0800,
                                        ipv4_src=src_ip,
                                        ipv4_dst=dst_ip)

                # Drop rule (no actions)
                self.add_flow(datapath, 100, match, [])
                return

        # Forwarding logic
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # Install flow rule
        match = parser.OFPMatch(in_port=in_port,
                               eth_dst=dst,
                               eth_src=src)

        self.add_flow(datapath, 1, match, actions)

        # Send packet
        out = parser.OFPPacketOut(datapath=datapath,
                                 buffer_id=msg.buffer_id,
                                 in_port=in_port,
                                 actions=actions,
                                 data=msg.data)
        datapath.send_msg(out)