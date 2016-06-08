from django.test import TestCase
from main.models import Effect, Sheet, Skill
from main.default_data import main
from collections import defaultdict


class Effect_Test(TestCase):
    
    def setUp(self):
        main()
        sheet = Sheet(owner_id=0, disp_base_str='10', disp_base_dex='12',
                      disp_base_con='14', disp_base_int='16',
                      disp_base_wis='18', disp_base_cha='20',
                      disp_base_fort='5', disp_base_ref='5', disp_base_will='5',
                      name='test_sheet')
        sheet.save()
        supers = [{'skill_bonus_id':10,
                   'bonus_amount':2,
                   'bonus_type':0,
                   'name':'test_sub_effects',
                   'owner':sheet},
                  {'skill_bonus_id': 13,
                   'bonus_amount': 2,
                   'bonus_type': 0,
                   'name': 'test_sub_effects2',
                   'owner': sheet}
                  ]
        supers_list = []
        for s in supers:
            super = Effect(skill_bonus_id=s['skill_bonus_id'],
                           bonus_amount=s['bonus_amount'],
                           bonus_type=s['bonus_type'],
                           name=s['name'],
                           sheet=s['owner'])
            super.save()
            supers_list.append(super)
        parent=supers_list[0]
        subs = [{'skill_bonus_id':11,
                 'bonus_amount':5,
                 'bonus_type':1,
                 'parent_effect': parent},
                {'save_bonus': 0,
                 'bonus_amount': 3,
                 'bonus_type': 1,
                 'parent_effect': parent},
                {'save_bonus': 1,
                 'x_to_y_bonus_ability': 3,
                 'bonus_type': 1,
                 'parent_effect': parent},
                {'save_override': 2,
                 'override_ability': 2,
                 'bonus_type': 1,
                 'parent_effect': parent}
                ]
        subs = [defaultdict(lambda: None, d) for d in subs]
        for s in subs:
            sub = Effect(skill_bonus_id=s['skill_bonus_id'],
                         bonus_amount=s['bonus_amount'],
                         bonus_type=s['bonus_type'],
                         parent_effect=s['parent_effect'],
                         save_bonus=s['save_bonus'],
                         save_override=s['save_override'],
                         x_to_y_bonus_ability=s['x_to_y_bonus_ability'],
                         override_ability=s['override_ability']
                         )
            sub.save()
                      
    def test_sub_effects(self):
        supes = Effect.objects.get(name='test_sub_effects')
        assert supes.skill_bonuses == {
            10: {0:[2]},
            11: {1:[5], 2:['Intelligence']},
        }

    def test_effects(self):
        sheet = Sheet.objects.get(name='test_sheet')
        effect = Effect.objects.get(name='test_sub_effects')
        skill = Skill.objects.get(id=11)
        print(sheet.fin_fort, sheet.fin_ref, sheet.fin_will)
        assert sheet.fin_fort == 10
        assert sheet.fin_ref == 9
        assert sheet.fin_will == 7
