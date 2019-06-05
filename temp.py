import json
import os


# for rid in os.listdir('./recipes/')[2:]:
#     text = None
#     obj = None
#     with open('./recipes/%s' %rid, 'r') as f:
#         print rid
#         text = f.read()
#         if text:
#             print text
#             text = text.split('\n')
#             line_count = len(text)
#             text = text[line_count/2-1:]
#             text[0] = text[0][1:]
#             # print '\n'.join(text)
#             # break
#             print text
#             obj = json.loads('\n'.join(text))
#         #         print rid
#     with open('./recipes/%s' % rid, 'w') as f:
#         if obj:
#             json.dump(obj, f, sort_keys=True,
#                    indent=4,
#                    separators=(',', ': '))


    #     try:
    #         recipe = json.load(f)
    #         recipe['id'] = rid
    #         json.dump(recipe, f, sort_keys=True,
    #             indent=4,
    #             separators=(',', ': '))
    #     except Exception as E:
    #         print 'empty recipe id: ', rid