
notes_on = []

count = {
    'line'      : 0,
    'event'     : 0,
    'bug'       : 0,
    'stuck'     : 0,
    'missed'    : 0,
    'black'     : 0,
    'white'     : 0,
    'notes'     : {},
    'bad_notes' : {}
}

def diagnose(line):
    note = line.rstrip()[-3:].strip()
    if note in count['notes'].keys():
        count['notes'][note] += 1
    else:
        count['notes'][note] = 1
 
    # nota se pali
    if "On" in line:
        # ali stoji upaljena od ranije
        if note in notes_on:
            # ispisi problematiku
            count['bug'] += 1 
            count['stuck'] += 1
            black_white_count(note)
            print('{0:<3} nota na liniji {1:<5} se zaglavila! velocity: {2}'.format(
                note, 
                find_problem(note),
                line[14:16] 
            ))
        # regularno
        else:
            # zabelezim da se upalila
            notes_on.append(note)

    # nota se gasi
    if "Off" in line:
        # nakon sto se upalila (regularno)
        if note in notes_on:
            # zabelezim da se ugasila
            notes_on.remove(note)
        # bez da se upalila
        else:
            # ispis problematiku
            count['bug'] += 1 
            count['missed'] += 1
            black_white_count(note)
            print('{0:<3} nota na liniji {1:<5} je promasena!'.format(note, count['line']))

def find_problem(note):
    i = count['line'] - 2
    while(note not in Lines[i]):
        i -= 1
    return i + 1

def black_white_count(note):
    if note in count['bad_notes'].keys():
        count['bad_notes'][note] += 1
    else:
        count['bad_notes'][note] = 1
    if '#' in note:
        count['black'] += 1
    else:
        count['white'] += 1

def recap():
    total = (count['event'] + count['bug']) // 2
    print('\n Od {0} odsviranih nota {1} ( {2:.2f}%) je zabagovalo! Od toga:'.format(
        total,
        count['bug'],
        100 * count['bug'] / total
    ))
    if count['bug']:
        print('\n Zaglavljenih: {0} ({2:.1f}%)   Promasenih: {1} ({3:.1f}%)'.format(
            count['stuck'], count['missed'],
            100.0 * count['stuck'] / count['bug'],
            100.0 * count['missed'] / count['bug']
        ))
        print('\n Crnih: {0}({2:.1f}%)   Belih: {1}({3:.1f}%)'.format(
            count['black'], 
            count['white'],
            100.0 * count['black'] / count['bug'],
            100.0 * count['white'] / count['bug']
        ))
        print('\n Po notama:\n Nota | Odsviranih | Losih ( % )')
        print('--------------------------------')
        for note in count['notes'].keys():
            played = count['notes'][note]
            bad = 0
            if note in count['bad_notes'].keys():
                bad = count['bad_notes'][note]
            print(' {0:<4} | {1:^10} | {2} ( {3:.2f}% )'.format(
                note, 
                (played + bad)//2, 
                bad, 
                200*bad/(bad+played)
            ))
    else: 
        print('\n Nota | Odsviranih ( % ) \n-------------------------')
        for note in count['notes'].keys():
            played = count['notes'][note] // 2
            print(' {0:<4} | {1} ( {2:.2f}% )'.format(
                note, 
                played, 
                100*played/total
            ))


# VOZI MISKO
with open('midi.txt') as fp:
    Lines = fp.readlines()

print('\n')
for line in Lines:
    count['line'] += 1
    if "Note" in line:
        count['event'] += 1
        diagnose(line)

recap()
