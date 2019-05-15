inputlist = get_ipython().getoutput("(ls hw1/)")
count = 0
for i in inputlist:
    str1 = "python3 hw2_0416235.py -i hw1/" + i + " -o rst" + str(count) + ".yml "
    #print(str1)
    get_ipython().system('$str1')
    print("-"*30)
    count = count + 1
