class SimpleGradebook(object):
    """
    前もってわかってない学生集団の成績を記録できるクラス
    """
    def __init__(self):
        self._grades = {}
    
    def add_student(self, name):
        self._grades[name] = []

    def report_grade(self, name, score):
        self._grades[name].append(score)

    def average_grade(self, name):
        grades = self._grades[name]
        return sum(grades) / len(grades)

book = SimpleGradebook()
book.add_student('molpako')
book.report_grade('molpako', 90)
book.report_grade('molpako', 80)
book.report_grade('molpako', 70)
print(book.average_grade('molpako'))

# SimpleGradebookクラスを拡張して科目ごとの成績リストを管理できるようにする
# それは _grades が学生の名前から別の辞書へマップするように変更することで実現できる
class BySubjectGradebook(object):
    def __init__(self):
        self._grades = {}
    
    def add_student(self, name):
        self._grades[name] = {}
    
    def report_grade(self, name, subject, grade):
        by_subject  = self._grades[name]
        grade_list = by_subject.setdefault(subject, [])
        grade_list.append(grade)
    
    def average_grade(self, name):
        by_subject = self._grades[name]
        total, count = 0, 0
        for grades in by_subject.values():
            total += sum(grades)
            count += len(grades)
        return total / count


book = BySubjectGradebook()
book.add_student('molpako')
book.report_grade('molpako', 'Math', 75)
book.report_grade('molpako', 'Math', 65)
book.report_grade('molpako', 'Gym', 90)
book.report_grade('molpako', 'Gym', 95)
print(book.average_grade('molpako'))

# クラスの最終成績に対して各点数に重みを与えて中間および最終テストの成績を重視する
# 科目をマップする成績の値を (score, weight) に変える
class WeightedGradebook(object):
    def __init__(self):
        self._grades = {}
    
    def add_student(self, name):
        self._grades[name] = {}
    
    def report_grade(self, name, subject, score, weight):
        by_subject  = self._grades[name]
        grade_list = by_subject.setdefault(subject, [])
        grade_list.append((score, weight))
    
    def average_grade(self, name):
        by_subject = self._grades[name]
        score_sum, score_count = 0, 0
        for subjcet, scores in by_subject.values():
            subjcet_avg, total_weight = 0, 0
            for score, weight in scores:
               subjcet_avg += score * weight 
               total_weight += weight

            score_sum += subjcet_avg / total_weight
            score_count += 1

        return score_sum /score_count 


# 入れ子が二段以上になり複雑になるならクラスに分割する
# まず依存性ツリーの最下部にある個々の成績からクラス化する
import collections
Grade = collections.namedtuple('Grade', ('score', 'weight'))

# 科目のクラス化
class Subject(object):
    def __init__(self):
        self._grades = []
    
    def report_grade(self, score, weight):
        self._grades.append(Grade(score, weight))
    
    def average_grade(self):
        total, total_weight = 0, 0
        for grade in self._grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight

# 学生が勉強している科目のクラス化
class Student(object):
    def __init__(self):
        self._subjects = {}
    
    def subject(self, name):
        if name not in self._subjects:
            self._subjects[name] = Subject()
        return self._subjects[name]
    
    def average_grade(self):
        total, count = 0, 0
        for subject in self._subjects.values():
            total += subject.average_grade()
            count += 1
        return total / count

# 学生のコンテナ
class Gradebook(object):
    def __init__(self):
        self._students = {}

    def student(self, name):
        if name not in self._students:
            self._students[name] = Student()    
        return self._students[name]

book = Gradebook()
molpako = book.student('molpako')
math = molpako.subject('Math')
math.report_grade(80, 0.10)
math.report_grade(90, 0.10)
math.report_grade(10, 0.80)
print(molpako.average_grade())

# 値がほかの辞書や長いタプルであるような辞書はつくらない
# 完全なクラスの柔軟性が必要となる前は軽量でミュータブルな namedtuple を使う
# 内部状態辞書が複雑になったら記録管理コードを複数のヘルパークラスを使うように変更する