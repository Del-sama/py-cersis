import argparse
import csv
import os
import typing

from collections import namedtuple as nt

Parser = argparse.ArgumentParser()
Problems = nt('Problems', 'question answer')


class QuizException(Exception):
    """ Something went wrong while running the quiz """



def main():
    Parser.add_argument("-csv", default="problems.csv",
                        help="csv file in the format: `question,answer`")
    Parser.add_argument("-limit", default=30, help="Integer time limit",
                        type=int)
    args = Parser.parse_args()
    filename = args.csv
    limit = args.limit
    assert os.stat(filename).st_size != 0

    if _is_valid_filename(filename):
        problems = _parse_csv(filename)
        quiz(problems, limit)


def quiz(problems, limit):
    correct = 0
    for idx, problem in enumerate(problems):
        print(f"Question number {idx+1} is {problem.question}? ")
        response = input()
        if response == problem.answer:
            correct += 1



def _is_valid_filename(filename: str) -> bool:
    if len(filename) < 5:
        return False
    if filename[-4:] != ".csv":
        return False
    if not filename[:-4].isalpha():
        return False
    return True


def _parse_csv(filename: str) -> typing.List[Problems]:
    try:
        rows = list(_read_csv(filename))
    except FileNotFoundError as exc:
        raise QuizException(f"filename `{filename}` does not exist") from exc
    problems_list = []
    for arr in rows:
        assert len(arr) == 2
        problems_list.append(Problems(arr[0], arr[1]))
    return problems_list


def _read_csv(filename: str) -> typing.List[str]:
    with open(filename, 'r') as csv_file:
        next(csv_file)
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            yield row

if __name__=="__main__":
    main()
