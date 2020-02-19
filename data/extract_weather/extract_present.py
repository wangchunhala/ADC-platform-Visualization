

file = open('./result data/warn.txt', 'r')
contents = file.read()
lines = contents.split('\n')
if lines[-1] == '':
    lines = lines[:-1]

end_list = ['解除', '取消', '预计']
present_line = []
for line in lines:
    items = line.split('\t')
    content = items[3]
    content = content.replace("取消", "，取消").replace("，，取消", "，取消")
    content = content.replace("预计", "，预计").replace("，，预计", "，预计")
    sentences = content.split('，')
    flag = 0
    for word in end_list:
        if sentences[0].find(word) != -1:
            flag = 1
            break
    if flag == 0:
        subcontent = ''
        for sentence in sentences:
            flag2 = 0
            for word in end_list:
                if sentence.find(word) != -1:
                    flag2 = 1
                    break
            if flag2 == 1:
                break
            else:
                subcontent += (sentence + '，')
        present_line.append(subcontent.replace(' ', '').replace('\t', ''))
    else:
        present_line.append('Null')

file = open('./result data/warn_present.txt', 'w')
for item in present_line:
    file.write(item + '\n')
file.close()