# Function to process a single input
def process_single_input(user_input):
    if user_input.startswith('"') and user_input.endswith('"'):
        processed_input = user_input[1:-1]
        return 1,processed_input
    else:
        return 0,user_input
    

# Function to process two inputs
def process_two_inputs(user_input1, user_input2):
    def format_input(user_input):
        if user_input.startswith('"') and user_input.endswith('"'):
            processed_input = user_input[1:-1]
            return 1,processed_input
        else:
            return 0,user_input
    
    ch,formatted_input1 = format_input(user_input1)
    
    ck,formatted_input2 = format_input(user_input2)
    return formatted_input1,formatted_input2,ch,ck
    
# Main function to process user inputs
def main(inputs):
    inputs = inputs.split('|')

    if len(inputs) == 1:
        ch,k = process_single_input(inputs[0].strip())
        if ch == 1:
            return k, " ", ch,0
        else:
            return k, " ", ch,0
    elif len(inputs) == 2:
        formatted_input1,formatted_input2,ch,ck = process_two_inputs(inputs[0].strip(), inputs[1].strip())
        return formatted_input1,formatted_input2,ch,ck
    else:
        print("Invalid input format. Please provide one or two inputs.")

if __name__ == "__main__":
    main()
