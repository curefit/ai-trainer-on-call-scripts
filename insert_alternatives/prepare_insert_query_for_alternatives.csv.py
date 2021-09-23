import csv


def get_rows(filename):
    with open(filename) as f:
        rows = list(csv.reader(f, delimiter=','))
    return rows


def main():
    rows = get_rows("new_alternatives.csv")

    with open("final_query.txt", "w") as f:
        f.write(
            'insert into alternative_exercise_mapping(tenant_id, hercules_exercise_id, alternative_type, hercules_alternative_exercise_id)')
        f.write('\n')
        f.write(f'values')
        f.write('\n')

        cnt = len(rows)
        for i, row in enumerate(rows):
            query = f"(1, '{row[1]}', '{row[4]}', '{row[3]}'){',' if i < cnt - 1 else ';'}"
            f.write(query)
            if i < cnt - 1:
                f.write('\n')


if __name__ == '__main__':
    main()
