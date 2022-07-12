import os
import sys

# Check Service is OK.
def service_test():
    status = os.system('systemctl is-active --quiet nuoj-database')
    print(status)

    if status != 0:
        print("service test failed.")
        sys.exit(1)

    print("service test passed.")

service_test()