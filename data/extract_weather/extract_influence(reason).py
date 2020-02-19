file = open('./result data/warn.txt', 'r')
contents = file.read()
lines = contents.split('\n')
if lines[-1] == '':
    lines = lines[:-1]

influence_line = []
influence_pre_or_future = []
for line in lines:
    items = line.split('\t')
    content = items[3]
    sentences = content.split('，')
    target_sentence = sentences[0]
    if target_sentence.find("受") != -1 and target_sentence.find("影响") != -1:
        influence_line.append(target_sentence)
        if sentences[1].find("预计"):
            influence_pre_or_future.append(2)
        else:
            influence_pre_or_future.append(1)
    else:
        influence_line.append("Null")
        influence_pre_or_future.append(0)

file = open('./result data/warn_influence.txt', 'w')
for i in range(len(influence_line)):
    file.write(influence_line[i] + '\t' + str(influence_pre_or_future[i]) + '\n')
file.close()