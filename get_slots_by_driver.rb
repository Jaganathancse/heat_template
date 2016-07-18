#!/usr/bin/ruby -w
#To get the slot details by driver name

#To get slots by driver name
def get_slots_by_drivers()
	drivers_details=%x{lspci -Dvmmkn}
	drivers_lines=drivers_details.split("\n")
	if(drivers_lines[drivers_lines.length-1].include? ":")
		drivers_lines.push(" ")
	end

	drivers=Hash.new
	slot=""
	driver="(none)"
	drivers_lines.each do |line|
		if line.include? ":"
			if line.include? "Slot" 
				line.slice! "Slot:"
				slot=line.strip
			elsif line.include? "Driver" 
				line.slice! "Driver:"
				driver=line.strip
			end
		else	
			if drivers.key?(driver)
				drivers[driver]=drivers[driver]+","+slot
			elsif 
				drivers[driver]=slot
			end		
		end
	end
	return drivers
end

#Creates hash and holds slots by driver name, key is driver name and slots are available in value field
drivers=Hash.new
drivers=get_slots_by_drivers()

drivers.each do |key,value|
	puts "pci_address_driver_"+key+"=>"+value+"\n"
end
