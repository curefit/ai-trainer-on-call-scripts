import csv


def get_rows(file_name):
    with open(file_name) as f:
        user_ids = list(csv.reader(f, delimiter=','))[1:]
    return user_ids


def get_unique_name(exercise_id, arr):
    for id, unique_name in arr:
        if exercise_id == id:
            return unique_name


def main():
    a = get_rows('alternatives_v1.csv')
    b = get_rows('exercise_id_to_title.csv')
    c = []

    for a1 in a:
        exercise_id = a1[0]
        exercise_unique_name = get_unique_name(exercise_id, b)
        alternative_type = a1[1]
        alternative_exercise_id = a1[2]
        alternative_exercise_unique_name = get_unique_name(alternative_exercise_id, b)
        c.append([exercise_id, exercise_unique_name, alternative_type, alternative_exercise_id, alternative_exercise_unique_name])

    fields = [
        'exercise_id',
        'exercise_unique_name',
        'alternative_type',
        'alternative_exercise_id',
        'alternative_exercise_unique_name'
    ]

    with open('final_alternatives.csv', 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(fields)
        csv_writer.writerows(c)


main()
