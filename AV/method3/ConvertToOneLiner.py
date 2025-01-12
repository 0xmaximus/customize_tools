import sys

def convert_to_oneliner(input_file, output_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    # Concatenate all lines and remove empty ones
    code = ''.join(line.strip() for line in lines if line.strip())

    # Remove unnecessary spaces around braces and make sure functions are written in a continuous flow
    code = code.replace(' {', '{').replace('} ', '}').replace('} {', '} {')  # Clean up spaces around {}
    
    # Write the result to the output file
    with open(output_file, 'w') as outfile:
        outfile.write(code)

# Command line interface for converting .ps1 to one-liner
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python convert.py <input.ps1> <output.ps1>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        convert_to_oneliner(input_file, output_file)
        print(f"Converted PowerShell script has been saved to {output_file}")
