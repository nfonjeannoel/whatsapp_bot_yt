json = []
namesCount = 0
center_details = "center_details"
center_name = "center_name"
student_and_results = "student_results"
papers_passed = "papers_passed"
center_details_text = ""
current_key = ""
paper_passed_index = -1
current_center = ""
current_num_papers = ""
name_builder = ""
number_counter = 0
build_name_flag = False
build_center_flag = False
center_builder = ""


def readResults():
    with open("result.txt", "r") as f:
        listResults = f.readlines()
    f.close()
    return listResults


def isCenterNumber(thisLine):
    global build_center_flag
    splitLine = thisLine.split()
    if "Centre" in splitLine or "No:" in splitLine:
        return True


def addCenterNumber(thisLine):
    global namesCount, json, current_center, number_counter
    number_counter = 0
    # centerCount += 1
    # json.append({})
    # json[namesCount][center_name] = thisLine
    current_center = thisLine
    # print(json[centerCount][thisLine])


def isCenterDetails(thisLine):
    global center_details_text
    splitLine = thisLine.split()
    if "Regist:" in splitLine or ("sat" in splitLine and "for:" in splitLine):
        center_details_text = line + ", "
        return True
    if "Sanctioned" in splitLine and "%" in splitLine:
        center_details_text = center_details_text + line

        return True
    return False


def addCenterDetails():
    global json, center_details
    # json[namesCount][center_details] = center_details_text
    # print(json[centerCount][center_details])


def isUselessLine(thisLine):
    splitLine = thisLine.split()
    return "Successful" in splitLine or "Candidates" in splitLine


def isNumberOfPapers(thisLine):
    splitLine = thisLine.split()
    return "Passed" in splitLine or "Subjects:" in splitLine


def addNumberOfPapers(thisLine):
    global json, current_key, paper_passed_index, current_num_papers, number_counter
    # json[namesCount][papers_passed] = thisLine
    number_counter = 0
    current_num_papers = thisLine
    # print(thisLine.strip('\n') + "curent")
    # print(json[centerCount][student_results][papers_passed])


def correctFormat(thisLine, nextLine):
    global name_builder, number_counter, build_name_flag
    studentNum = thisLine.split()[0]
    number = studentNum[1:len(studentNum) - 1]
    try:
        return type(int(number)) == int
    except ValueError:
        listName = nextLine.split()
        if len(listName[len(listName) - 1]) == 5 and len(listName[len(listName) - 2]) == 6:
            build_name_flag = True
            name_builder = line
        return False


def formatNumPapers(num_papers):
    papers = num_papers.split()[:4]
    final = ""
    for i in papers:
        final += i + " "
    return final + "(total = " + str(num_papers.split()[4:][0]) + ")"


def buildGrades(thisLine):
    global build_name_flag, name_builder, json, namesCount, number_counter

    number_counter += 1
    name_builder = "(" + str(number_counter) + ")" + " " + name_builder + " " + thisLine
    json.append({})
    json[namesCount][center_name] = current_center
    json[namesCount][center_details] = center_details_text
    json[namesCount][papers_passed] = formatNumPapers(current_num_papers)
    json[namesCount][student_and_results] = name_builder
    namesCount += 1

    build_name_flag = False


def addStudentNameAndGrades(thisLine, nextLine):
    global json, namesCount, number_counter, build_name_flag
    if build_name_flag is not True:
        if correctFormat(thisLine, nextLine):
            number_counter += 1
            json.append({})
            json[namesCount][center_name] = current_center
            json[namesCount][center_details] = center_details_text
            json[namesCount][papers_passed] = formatNumPapers(current_num_papers)
            json[namesCount][student_and_results] = "(" + str(number_counter) + ")" + " " + thisLine[4:]
            namesCount += 1

    else:
        buildGrades(thisLine)


def saveFile(my_json):
    with open("myjson.txt", "w") as f:
        f.writelines(my_json)


if __name__ == '__main__':
    results = readResults()
    for index, line in enumerate(results):
        line = line.strip('\n')
        line = line.replace(",", ", ")
        if isCenterNumber(line):
            addCenterNumber(line)
            continue

        if isCenterDetails(line):
            addCenterDetails()
            continue
        if isUselessLine(line):
            continue
        if isNumberOfPapers(line):
            addNumberOfPapers(line)
        else:
            if index + 1 <= len(results) - 1:
                next_line = results[index + 1].strip('\n')
                next_line = next_line.replace(",", ", ")
                # print(line)
                # print(next_line)
                # print("____")
                addStudentNameAndGrades(line, next_line)
            else:
                addStudentNameAndGrades(line, line)

    myJson = ""
    for ind, i in enumerate(json):
        myJson += "{" + "'" + center_name + "'" + " " + ":" + " " + "'" + i[center_name] + "'" + ","
        myJson +=  "'" + center_details + "'" + " " + ":" + " " + "'" + i[center_details] + "'" + ","
        myJson +=  "'" + papers_passed + "'" + " " + ":" + " " + "'" + i[papers_passed] + "'" + ","
        if ind < len(json) - 1:
            myJson +=  "'" + student_and_results + "'" + " " + ":" + " " + "'" + i[student_and_results] + "'" + "}" + ","
        else:
            myJson += "'" + student_and_results + "'" + " " + ":" + " " + "'" + i[student_and_results] + "'" + "}"
    myJson = "[" + myJson + "]"
    # print(myJson)
    saveFile(myJson)

