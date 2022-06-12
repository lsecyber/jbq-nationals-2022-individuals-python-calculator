import csv
from pathlib import Path
import pandas as pd


class QuizzerStats:
    """
    Creates a class for quizzer stats that includes different fields. Used to sort by quizzers.
    """
    def __init__(self, name_and_team, friday_place, saturday_place, total, average, num_of_rounds, quiz_outs, accuracy):
        self.nameAndTeam = name_and_team
        self.fridayPlace = friday_place
        self.saturdayPlace = saturday_place
        self.total = total
        self.avg = average
        self.numOfRounds = num_of_rounds
        self.quizOuts = quiz_outs
        self.accuracy = accuracy


def remove_percent(string_to_remove):
    """
    Removes percent symbol from the end of the string passed in.

    :param string_to_remove: String to remove the percent from the end or
    :return: str
    """
    string_to_remove = str.rstrip(string_to_remove, '%')
    return string_to_remove


def file_to_var(file: str, extension: str):
    """
    Returns a text strand of the file passed in.

    :param file: String of the filename
    :param extension: Stinrg of the file extension
    :return: str
    """
    return Path(f'files/{file}.{extension}').read_text()


def parse_file_to_data(file, extension, table_name):
    """
    Parses the file passed in.

    :param file: The file string
    :param extension: The extension of the file
    :param table_name: the table identifier
    :return: a list of the quizzers
    """
    temp_table = pd.read_html(file_to_var(file, extension), match=table_name, header=0,
                              converters={'Q%': remove_percent})
    df = temp_table[1]
    df_two = temp_table[0]
    df_two = df_two.fillna(0)
    df_two.to_html('files/testing.html')
    win_loss_array = df_two['W / L'][1].replace(' ', '').split('/')
    number_of_rounds = int(win_loss_array[0]) + int(win_loss_array[1])
    df = df.fillna(0)
    # df.to_html('files/testing.html')
    quizzers_return_me = {}
    for index, row in df.iterrows():
        quizzers_return_me[row['Quizzer'] + '; ' + row['Team / Church']] = {
            'Place': row['#'],
            'Total': row['- Total -'],
            'Avg': row['- AVG -'],
            'NumberOfRounds': number_of_rounds,
            'Q%': row['Q%'],
            'Quizouts': row['QO']
        }
    return quizzers_return_me


if __name__ == '__main__':
    fBlue = parse_file_to_data('f-blue', 'html', '- Total -')
    fGreen = parse_file_to_data('f-green', 'html', '- Total -')
    fYellow = parse_file_to_data('f-yellow', 'html', '- Total -')
    fPink = parse_file_to_data('f-pink', 'html', '- Total -')
    fLavender = parse_file_to_data('f-lavender', 'html', '- Total -')

    sBlue = parse_file_to_data('s-blue', 'html', '- Total -')
    sGreen = parse_file_to_data('s-green', 'html', '- Total -')
    sLavender = parse_file_to_data('s-lavender', 'html', '- Total -')
    sOrange = parse_file_to_data('s-orange', 'html', '- Total -')
    sPink = parse_file_to_data('s-pink', 'html', '- Total -')
    sSilver = parse_file_to_data('s-silver', 'html', '- Total -')
    sTan = parse_file_to_data('s-tan', 'html', '- Total -')
    sYellow = parse_file_to_data('s-yellow', 'html', '- Total -')

    totalFridayResults = {}
    totalFridayResults.update(fBlue)
    totalFridayResults.update(fGreen)
    totalFridayResults.update(fLavender)
    totalFridayResults.update(fPink)
    totalFridayResults.update(fYellow)

    totalSaturdayResults = {}
    totalSaturdayResults.update(sBlue)
    totalSaturdayResults.update(sGreen)
    totalSaturdayResults.update(sLavender)
    totalSaturdayResults.update(sOrange)
    totalSaturdayResults.update(sPink)
    totalSaturdayResults.update(sSilver)
    totalSaturdayResults.update(sTan)
    totalSaturdayResults.update(sYellow)

    totalResults = {}
    totalResults.update(totalFridayResults)
    for quizzer in totalResults:
        friQuizzer = totalFridayResults[quizzer]
        satQuizzer = totalSaturdayResults[quizzer]
        totalPoints = friQuizzer["Total"] + satQuizzer["Total"]
        totalRounds = friQuizzer["NumberOfRounds"] + satQuizzer["NumberOfRounds"]
        avg = round(totalPoints / totalRounds, 1)
        quizOuts = friQuizzer["Quizouts"] + satQuizzer["Quizouts"]
        totalResults[quizzer]["Total"] = totalPoints
        totalResults[quizzer]["Quizouts"] = quizOuts
        totalResults[quizzer]["Avg"] = avg
        totalResults[quizzer]["FridayPlace"] = friQuizzer["Place"]
        totalResults[quizzer]["SaturdayPlace"] = satQuizzer["Place"]
        totalResults[quizzer]["Accuracy"] = ((int(friQuizzer["Q%"]) + int(satQuizzer["Q%"])) / 2)

    totalResultsObjects = []
    for quizzer in totalResults:
        totalResultsObjects.append(QuizzerStats(
            name_and_team=quizzer,
            friday_place=totalResults[quizzer]["FridayPlace"],
            saturday_place=totalResults[quizzer]["SaturdayPlace"],
            total=totalResults[quizzer]["Total"],
            average=totalResults[quizzer]["Avg"],
            num_of_rounds=totalResults[quizzer]["NumberOfRounds"],
            quiz_outs=totalResults[quizzer]["Quizouts"],
            accuracy=totalResults[quizzer]["Accuracy"]
        ))
    totalResultsObjects.sort(key=lambda q: q.avg, reverse=True)

    x = 0
    with open('files/final_results.csv', 'w') as f:
        w = csv.writer(f)
        header = ['Place', 'Quizzer & Church', 'Avg', 'Total', 'Quizouts', 'Accuracy']
        w.writerow(header)

        for quizzerObject in totalResultsObjects:
            x += 1
            w.writerow([x, quizzerObject.nameAndTeam, quizzerObject.avg, quizzerObject.total, quizzerObject.quizOuts,
                        (str(quizzerObject.accuracy) + '%')])
