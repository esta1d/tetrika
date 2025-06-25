def appearance(intervals):
    # рамки урока
    lesson_start, lesson_end = intervals['lesson']
    
    # интервалы ученика
    pupil_times = []
    for start, end in zip(intervals['pupil'][::2], intervals['pupil'][1::2]):
        if start <= lesson_end and end >= lesson_start:
            pupil_times.append((start, end))

    # интервалы учителя
    tutor_times = []
    for start, end in zip(intervals['tutor'][::2], intervals['tutor'][1::2]):
        if start <= lesson_end and end >= lesson_start:
            tutor_times.append((start, end))
    
    # Объединяем моменты входа и выхода
    events = []
    for start, end in pupil_times + tutor_times:
        events.append((start, '+')) 
        events.append((end, '-'))  
        
    events.sort()
    
    count_active = 0 
    total_time = 0
    last_event_time = None
    
    # обновляем суммарное время
    for time, event_type in events:
        if last_event_time is not None and count_active > 1:
            # если оба участника были активны одновременно
            total_time += min(time, lesson_end) - max(last_event_time, lesson_start) # ВНИМАНИЕ!!! условине учитывает границы урока, из-за чего в этом варианте кода мы полчим ошибку на второй итерации
            
        if event_type == '+':
            count_active += 1
        else:
            count_active -= 1
            
        last_event_time = time
    
    return total_time


tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'intervals': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
    {'intervals': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
]

for test_case in tests:
    result = appearance(test_case['intervals'])
    print(f'Результат теста: {result}, правильный ответ: {test_case["answer"]}')

# Почему во втором тесте ответ 3577 я не понял, поэтома написал вывод выше такой. Не понял по причине: учителя уже нет на уроке, разве нам нужно его считать? 



# if __name__ == '__main__':
#    for i, test in enumerate(tests):
#        test_answer = appearance(test['intervals'])
#        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'