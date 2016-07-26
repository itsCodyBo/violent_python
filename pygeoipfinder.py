#1. pg 136 of Violent Python by TJ O'Connor

'''

#We are using the imported pygeoip module to search the database from
#http://dev.maxmind.com/geoip/legacy/geolite/ and match it with an ip address

import pygeoip

GI = pygeoip.GeoIP('/home/cody/workspace/violent_python/opt/GeoIP/GeoLiteCity.dat')

#output should be the location of the given ip; NOTE: does not work for IPV6

gi = pygeoip.GeoIP('/home/cody/workspace/violent_python/opt/GeoIP/GeoLiteCity.dat')
def printRecord(tgt):
	rec = gi.record_by_name(tgt)
	city = rec['city']
	region = rec['region_code']
	country = rec['country_name']
	long = rec['longitude']
	lat = rec['latitude']
	print '[*] Target: ' + tgt + ' Geo-located.'
	print '[+] ' +str(city)+','+str(lat)+ ',longitude: '+str(long)
tgt = '173.255.226.98'
printRecord(tgt)



#reading a pcap capture; NOTE: it would be useful to learn how to view live
#traffic via studying pypcap
import dpkt
import socket
def printPcap(pcap):
	for (ts,buf) in pcap:
		try:
			eth = dpkt.ethernet.Ethernet(buf)
			ip = eth.data
			src = socket.inet_ntoa(ip.src)
			dst = socket.inet_ntoa(ip.dst)
			print '[+] Src: ' + src + ' --> Dst: ' + dst
		except:
			pass
			
def main():
	f = open('geotest.pcap')
	pcap = dpkt.pcap.Reader(f)
	printPcap(pcap)
if __name__ == '__main__':
	main()


#create a new function that returns a pyschial location for an IP address
import dpkt, socket, pygeoip, optparse

gi = pygeoip.GeoIP("/home/cody/workspace/violent_python/opt/GeoIP/GeoLiteCity.dat")
def retGeoStr(ip):
	try:
		rec = gi.record_by_name(ip)
		city = rec['city']
		country = rec['country_code3']
		if (city != ''):
			geoLoc = city+' , '+country
		else:
			geoLoc = country
		return geoLoc
	except:
		return 'Unregistered'

'''

#2. this is the entire set up put together

import dpkt,socket,pygeoip,optparse
gi = pygeoip.GeoIP("/home/cody/workspace/violent_python/opt/GeoIP/GeoLiteCity.dat")
def retGeoStr(ip):
	try:
		rec = gi.record_by_name(ip)
		city = rec['city']
		country = rec['country_code3']
		if city != '':
			geoLoc = city + ',' + country
		else:
			geoLoc = country
		return geoLoc
	except:
		return 'Unregistered'
def printPcap(pcap):
	for (ts, buf) in pcap:
		try:
			eth = dpkt.ethernet.Ethernet(buf)
			ip = eth.data
			src = socket.inet_ntoa(ip.src)
			dst = socket.inet_ntoa(ip.dst)
			print '[+] Src: ' + src + '----> Dst: ' + dst
			print '[+] Src: ' +retGeoStr(src) + '----> Dst: ' + retGeoStr(dst)
		except:
			pass
			
def main():
	parser = optparse.OptionParser('usage%prog -p <pcap file>')
	parser.add_option('-p',dest='pcapFile',type='string',\
	help='specify pcap filename')
	(options,args) = parser.parse_args()
	if options.pcapFile == None:
		print parser.usage
		exit(0)
	pcapFile = options.pcapFile
	f = open(pcapFile)
	pcap = dpkt.pcap.Reader(f)
if __name__ == '__main__':
	main()

'''
Desiered output:


analyst# python geoPrint.py -p geotest.pcap
[
+
] Src: 110.8.88.36 --> Dst: 188.39.7.79
[
+
] Src: KOR --> Dst: London, GBR
[
+
] Src: 28.38.166.8 --> Dst: 21.133.59.224
[
+
] Src: Columbus, USA --> Dst: Columbus, USA
[
+
] Src: 153.117.22.211 --> Dst: 138.88.201.132
[
+
] Src: Wichita, USA --> Dst: Hollywood, USA
[
+
] Src: 1.103.102.104 --> Dst: 5.246.3.148
[
+
] Src: KOR --> Dst: Unregistered
[
+
] Src: 166.123.95.157 --> Dst: 219.173.149.77
[
+
] Src: Washington, USA --> Dst: Kawabe, JPN
[
+
] Src: 8.155.194.116 --> Dst: 215.60.119.128
[
+
] Src: USA --> Dst: Columbus, USA
[
+
] Src: 133.115.139.226 --> Dst: 137.153.2.196
[
+
] Src: JPN --> Dst: Tokyo, JPN
[
+
] Src: 217.30.118.1 --> Dst: 63.77.163.212
[
+
] Src: Edinburgh, GBR --> Dst: USA
[
+
] Src: 57.70.59.157 --> Dst: 89.233.181.180
[
+
] Src: Endeavour Hills, AUS --> Dst: Prague, CZE
'''

#3. we are going to build the kml document to map to google maps
