def main():
    req = open("requirements.txt")
    clean = ''
    for line in req:
        if '#' in line:
            clean += f"{line.split('#')[0].strip()}\n"
        else:
            clean += line
    req.close()
    
    newreq = open("requirements.txt","w")
    newreq.write(clean)
    newreq.close()
    
if __name__ == '__main__':
    main()