# 🚀 ARP Handling in SDN Networks using Mininet and Ryu Controller

---

## 📌 1. Project Overview

This project demonstrates the implementation of **Address Resolution Protocol (ARP) handling in Software Defined Networking (SDN)** using the **Ryu controller** and **Mininet emulator**.

Traditional networks rely on distributed control, where each switch independently decides packet forwarding. In contrast, SDN centralizes control logic in a controller, allowing dynamic and programmable network behavior.

This project showcases:

* ARP packet handling using a controller
* Dynamic flow rule installation
* Controlled communication (allow/block)
* Performance analysis using ping and iperf

---

## 🧠 2. Background Concepts

### 2.1 Software Defined Networking (SDN)

SDN separates:

* **Control Plane** → Decision making (Controller)
* **Data Plane** → Packet forwarding (Switch)

### Why SDN?

* Centralized control
* Easy programmability
* Flexible traffic management
* Dynamic network policies

---

### 2.2 Mininet

Mininet is a lightweight network emulator that:

* Creates virtual hosts, switches, and links
* Allows real network testing on a single machine

Components used:

* `h1`, `h2` → Hosts
* `s1` → Switch
* Links → Virtual connections

---

### 2.3 Ryu Controller

Ryu is a Python-based SDN controller that:

* Communicates via OpenFlow
* Handles packet events
* Installs flow rules dynamically

---

### 2.4 Address Resolution Protocol (ARP)

ARP maps:

```
IP Address → MAC Address
```

### Working:

1. Host sends ARP Request (broadcast)
2. Target host replies with MAC address

---

## ❗ 3. Problem Statement

Design an SDN-based solution that:

* Intercepts ARP packets
* Generates ARP responses
* Enables host communication
* Controls traffic using flow rules
* Demonstrates both **allowed and blocked scenarios**

---

## 🎯 4. Objectives

* Implement ARP handling using Ryu
* Enable communication between hosts
* Implement traffic blocking logic
* Analyze performance using ping and iperf

---

## 🛠 5. Tools & Technologies Used

| Tool           | Purpose                   |
| -------------- | ------------------------- |
| Mininet        | Network simulation        |
| Ryu Controller | SDN logic                 |
| OpenFlow       | Communication protocol    |
| Python         | Controller implementation |
| iperf          | Throughput measurement    |
| ping           | Latency measurement       |

---

## 🌐 6. Network Topology

Topology used: **Single Switch Topology**

```
h1 ---- s1 ---- h2
```

### Components:

* 1 Switch → `s1`
* 2 Hosts → `h1`, `h2`

### Working:

* All traffic passes through switch
* Switch forwards packets based on controller rules

---

## ⚙️ 7. Approach & Design Decisions

### 🔍 Why this approach?

We used a **controller-based ARP handling approach** because:

* Centralized logic simplifies control
* Easy to modify behavior (e.g., block traffic)
* Demonstrates SDN advantages clearly

---

### 🧠 Why Ryu?

* Lightweight and Python-based
* Easy to implement logic
* Widely used in SDN labs

---

### 🔧 Why Flow Rules?

Instead of forwarding every packet manually:

* Install rules → faster processing
* Reduces controller load
* Improves performance

---

### 🚫 Why Blocking Scenario?

To demonstrate:

* Network control capability
* Policy enforcement
* Real-world SDN use cases (firewalls, filtering)

---

## ⚙️ 8. Implementation Details

### Controller Logic

The controller performs:

1. **Packet Interception**

   * Switch sends unknown packets to controller

2. **MAC Learning**

   * Learns host MAC addresses

3. **ARP Handling**

   * Detects ARP packets
   * Logs ARP requests

4. **Flow Rule Installation**

   * Match conditions → actions
   * Installed using OpenFlow

5. **Blocking Logic**

   * Blocks traffic from:

     ```
     h1 → h2
     ```

---

## 🧪 9. Execution Steps & Commands

---

### 🔹 Step 1: Activate Environment

```bash
source ryu-env/bin/activate
```

---

### 🔹 Step 2: Start Controller

```bash
ryu-manager arp_controller.py
```

---

### 🔹 Step 3: Start Mininet

```bash
sudo mn --controller=remote
```

---

### 🔹 Step 4: Network Test

```bash
pingall
```

👉 Output:

* 0% packet loss
* All hosts reachable

---

### 🔹 Step 5: Host Communication

```bash
h1 ping h2
```

👉 Output:

* Successful communication
* Low latency

---

### 🔹 Step 6: Blocking Scenario

```bash
h1 ping h2
```

👉 Output:

* Destination Host Unreachable
* Communication blocked

---

### 🔹 Step 7: Throughput Test

```bash
h2 iperf -s &
h1 iperf -c h2
```

👉 Output:

* Bandwidth in Gbps

---

### 🔹 Step 8: Flow Table

```bash
sudo ovs-ofctl dump-flows s1
```

👉 Output:

* Flow rules installed

---

### 🔹 Step 9: Additional Commands

```bash
net
nodes
dump
```

---

## 🧪 10. Test Scenarios

### ✅ Scenario 1: Normal Communication

* ARP resolved successfully
* Packets forwarded
* Communication works

---

### 🚫 Scenario 2: Blocked Communication

* Controller installs DROP rule
* Packets not forwarded
* Communication fails

---

## 📊 11. Performance Analysis

### 📉 Latency (Ping)

* Very low (milliseconds)
* Indicates efficient communication

---

### 📈 Throughput (iperf)

* High bandwidth observed
* Confirms good performance

---

## 📋 12. Flow Table Analysis

Flow entries define:

* Match conditions (IP, MAC)
* Actions (forward/drop)

Example:

```
priority=1,in_port=1 actions=output:2
```

---

## 📸 13. Screenshots

Include:

* Mininet startup
* pingall output
* h1 ping h2 (success)
* blocked output
* iperf output
* flow table
* controller logs

---

## 📌 14. Results & Observations

* ARP successfully handled by controller
* Dynamic flow rule installation works
* Blocking logic successfully implemented
* SDN provides flexible control

---

## ✅ 15. Conclusion

This project demonstrates how SDN enables:

* Centralized control
* Dynamic rule installation
* Flexible traffic management

The Ryu controller effectively handles ARP and controls communication, showcasing the power of SDN.

---

## 📚 16. References

* Ryu Documentation
* Mininet Documentation
* OpenFlow Specification

---

## 💯 Final Outcome

✔ Working SDN network
✔ ARP handled via controller
✔ Traffic control implemented
✔ Performance analyzed

---

🔥 This project successfully demonstrates real-world SDN concepts.
