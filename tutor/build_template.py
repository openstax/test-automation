#!/usr/bin/python3

"""Create a templatized file for a test epic file."""
from getopt import getopt, GetoptError
import sys


def main(argv):
    # print('Check Arguments: %s' % argv)
    output_file = None
    debug = False
    products = {
        't1': 'Tutor v1',
        't2': 'Tutor v2',
        't3': 'Tutor v3',
        't4': 'Tutor v4',
        'cc1': 'Concept Coach v1',
        'cc2': 'Concept Coach v2',
        'cc3': 'Concept Coach v3',
        'cc4': 'Concept Coach v4',
    }
    try:
        opts, args = getopt(
            argv,
            'ho:p:e:n:c:v',
            [
                'help',
                'ofile=',
                'product=',
                'epic=',
                'epic-name=',
                'case-list='
            ]
        )
    except GetoptError as e:
        print('build_template.py -o <outputfile> <options>')
        print('Use "-h" or "--help" for a list of options.')
        # print(argv)
        print(e)
        sys.exit(2)
    print('Processing Arguments...')
    for opt, arg in opts:
        print('    %s :: %s' % (opt, arg))
        if opt in ('-h', '--help'):
            print('OpenStax Tutor Template Builder')
            print('===============================')
            print('    -h / --help         Display this help text')
            print('    -o / --ofile        Output file name if different ' +
                  'from camel-case "epic-name" without whitespace')
            print('    -p / --product      Product')
            print('    -e / --epic         Epic number')
            print('    -n / --epic-name    Full epic text')
            print('    -c / --case_list    A comma-separated list of ' +
                  'TestRail case IDs')
            print(' ')
            sys.exit(0)
        elif opt in ('-o', '--ofile'):
            output_file = arg
        elif opt in ('-p', '--product'):
            product = arg.lower()
        elif opt in ('-e', '--epic'):
            epic_number = arg
        elif opt in ('-n', '--epic-name'):
            epic_name = arg
        elif opt in ('-c', '--case_list'):
            case_list = arg.split(',')
        elif opt in ('-v'):
            debug = True
        else:
            print('Unknown argument: %s :: %s' % (opt, arg))
            sys.exit(2)
    print('\n************************************')
    if debug:
        print('Read lead in file template.')
    output_file = output_file if output_file else \
        'test_{0}_{1}_{2}.py'.format(
            product,
            epic_number.zfill(2),
            str.replace(epic_name.title().strip(), ' ', '')
        )
    output = ''
    case_text = ''
    with open('./template_lead_in.txt', 'r') as lead_in:
        output = lead_in.read()
    if debug:
        print('Replace placeholders')
    case_list_format = ''
    for index, case in enumerate(case_list):
        if index == 0:
            case_list_format = '' + case
            continue
        split = ', ' if index % 5 != 0 else ',\n        '
        if debug:
            print('Split: %s  "%s"' % (index, split))
        case_list_format = case_list_format + split + case
    output = output.format(
        Product_Full=products[product],
        Product=product.upper(),
        Epic=epic_number,
        Epic_Text=epic_name.title(),
        list_of_cases=case_list_format,
        File_Epic=str.replace(epic_name.title().strip(), ' ', ''),
        basic_env="""{
    'platform': 'OS X 10.11',
    'browserName': 'chrome',
    'version': '50.0',
    'screenResolution': "1024x768",
}"""
    )

    if debug:
        print('Read test case file template')
    with open('./template_case_list.txt', 'r') as case_outline:
        case_text = case_outline.read()
    if debug:
        print('Replace placeholders')
    for story_number, case in enumerate(case_list):
        print('    Story %s' % str(story_number + 1))
        temp = case_text
        if debug:
            print('    - write temp')
        temp = temp.format(
            CaseID=case,
            product=product.lower(),
            epic=epic_number,
            story=str(story_number + 1).zfill(3)
        )
        print('\n%s\n************************************' % temp)
        output = output + temp

    if debug:
        print('Write output file')
    with open(output_file, 'w') as ofile:
        ofile.write(output)

if __name__ == '__main__':
    main(sys.argv[1:])
