import oci
import logging
import os

# Environment variable BURSTSCRIPT_HOME is required before running the program.
workdir = os.getenv('BURSTSCRIPT_HOME')

logging.basicConfig(filename=workdir + os.path.sep + "logs" + os.path.sep + "output.log", 
					format='%(asctime)s %(message)s', 
					filemode='a')
logger = logging.getLogger() 
logger.setLevel(logging.INFO) 
logger.debug("Program home dir is {workdir}".format(workdir = workdir))

# Create a config using DEFAULT profile
config = oci.config.from_file(file_location=workdir + os.path.sep + "oci_auth.conf")

# Initialize service client with default config file
core_client = oci.core.ComputeClient(config)

# Update a single instance
def updateInstanceShape(instId, baseline, ocpus, memory_in_gbs):
    logger.info("Updating VM {vm} with CPU utilization baseline {pct}".format(vm = instId, pct=baseline))

    # get_instance_response = core_client.get_instance(
    #     instance_id=instId)
    # # Get the data from response
    # print(get_instance_response.data)

    update_instance_response = core_client.update_instance(
        instance_id=instId,
        update_instance_details=oci.core.models.UpdateInstanceDetails(
            shape_config=oci.core.models.UpdateInstanceShapeConfigDetails(
                ocpus=ocpus,
                memory_in_gbs=memory_in_gbs,
                baseline_ocpu_utilization=baseline)))

    # Display something
    respStatus = update_instance_response.status
    instName = update_instance_response.data.display_name
    logger.info("Changing the shape for VM {vm}, {ocpus}, {mems}, Status is {status}"
        .format( vm = instName, ocpus = ocpus, mems = memory_in_gbs, status = respStatus))

# Update a instances listed in the vm.ini file.
def updateAll(Burstable = False):
    ocidConfFile = workdir + os.path.sep + "vm.ini"
    updVmCount = 0
    with open(ocidConfFile, 'r') as file:
        line = file.readline()
        while line:
            line = line.strip()
            if len(line) > 0 and not line.startswith('#'):
                args = line.split()
                restoreBaseline = "BASELINE_1_1"
                if len(args) >= 5:
                    restoreBaseline = args[4]
                updateInstanceShape(args[0], args[1] if Burstable else restoreBaseline, float(args[2]), float(args[3]))
                updVmCount += 1
            line = file.readline()
    logger.info("Done. Totally updated {count} instances.".format(count = updVmCount))