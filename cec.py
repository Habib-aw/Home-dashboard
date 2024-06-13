import subprocess

def switch_hdmi(input_number):
    # The HDMI port mappings may need to be adjusted based on your setup
    input_map = {
        1: '10:00',  # HDMI 1
        2: '20:00',  # HDMI 2
        # Add more mappings if needed
    }

    if input_number not in input_map:
        print(f"Invalid HDMI input: {input_number}")
        return

    command = f"echo 'tx 4F:82:{input_map[input_number]}' | cec-client -s -d 1"
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Command executed successfully")
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print("Error executing command")
        print(e.stderr.decode())
