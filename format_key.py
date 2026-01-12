
def format_key():
    with open('student_public.pem', 'r') as f:
        key = f.read().strip()
    
    # Replace newlines with literal \n characters
    single_line = key.replace('\n', '\\n')
    print(single_line)

if __name__ == "__main__":
    format_key()
