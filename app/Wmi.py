from subprocess import call
username="HCTRA-TMC\\admministrator"
password="UTSinc2010"
host="10.40.18.12"
query ="SELECT * FROM Win32_Processor"

call(["wmic", "-UHCTRA-TMC\\administrator%password 'select * from win32_operatingsystem'"])
