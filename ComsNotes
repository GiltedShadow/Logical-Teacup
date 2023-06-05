 Binary count vs pins needed
___|________________|_______________|_______________|______________
  1|	000000	     	17|	010000	    	33|	100000	  	  49|	110000
  2|	000001 --1   18|	010001	    	34|	100001	  	  50|	110001
  3|	000010	     	19|	010010	   	 35|	100010	  	  51|	110010
  4|	000011 --2   20|	010011	   	 36|	100011	  	  52|	110011
  5|	000100	     	21|	010100	   	 37|	100100	  	  53|	110100
  6|	000101	     	22|	010101	   	 38|	100101	  	  54|	110101
  7|	000110	     	23|	010110	   	 39|	100110	  	  55|	110110
  8|	000111 --3	  24|	010111	   	 40|	100111	  	  56|	110111
  9|	001000	     	25|	011000	   	 41|	101000	  	  57|	111000
 10|	001001	     	26|	011001	   	 42|	101001	  	  58|	111001
 11|	001010    	 	27|	011010	   	 43|	101010	  	  59|	111010
 12|	001011	     	28|	011011	   	 44|	101011	  	  60|	111011
 13|	001100	     	29|	011100	   	 45|	101100	  	  61|	111100
 14|	001101	     	30|	011101	   	 46|	101101	    	62|	111101
 15|	001110	     	31|	011110		    47|	101110	    	63|	111110
 16|	001111 --4  	32|	011111 --5	 48|	101111	    	64|	111111 --6

When using this as communication, theoretically there would be an infinite amount of messages or commands to receive or exchange data

the plan is to use x number of pins to count in binary, with an extra pin used as an "acknowledged" flash, then the information communicated can be confirmed by the receiver repeating the information

this can happen at ever step or at the very end of the communication line

There should always be a "start communication" and an "end communication" binary number in order to begin and finilize data

 1-a   | 11-k   | 21-u   | 31-start
 2-b   | 12-l   | 22-v   | 32-end
 3-c   | 13-m   | 23-w   | 
 4-d   | 14-n   | 24-x   | 
 5-e   | 15-o   | 25-y   | 
 6-f   | 16-p   | 26-z   | 
 7-g   | 17-q   | 27-    | 
 8-h   | 18-r   | 28-.   | 
 9-i   | 19-s   | 29-,   | 
10-j   | 20-t   | 30-number

can use the 1-10 and a special beginning input to change from latters to numbers
using 27 as a space, 5 pins give a max of 32 inputs so there is room for a period and comma, with room for a number switch and a start and end specific command

only using the 29 inputs, even with no repeating characters and only 3 characters there are almost 22k commands or translations available

with 2 non repeating characters, 700 actions are available

note- above is using 5 pins to transfer binary, if we reduce that to 4 pins there would be 16 available, so with 2 just about 196 commands, and with 3 2700 are available if we leave 2 for start and finish
with 3 pins 1-8, 2 inputs would be 36, 3 is 216, and 4 is 1296 leaving out the start and finish
so it might be fairly easy to reduce the binary pins to 3 so only 4 woujld be used, limiting the pins needed for communication and allowing plenty of pins to be used for actual usage for things




what about UART?

only 2 pins would be needed, plus a ground but that can be included elsewhere
I beleive a significant portion of data can be transferred easily through these 2 pins, and can just use a micro or mini usb instead of full custom pinning

https://docs.arduino.cc/learn/built-in-libraries/software-serial
https://www.contec.com/support/basic-knowledge/daq-control/serial-communicatin/
