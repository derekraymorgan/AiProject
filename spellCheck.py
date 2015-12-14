
import re
import collections

'''
argmaxc P(w|c) P(c)
There are three parts of this expression. From right to left, we have:

P(c), the probability that a proposed correction c stands on its own. This is called the language model: think of it as
answering the question "how likely is c to appear in an English text?" So P("the") would have a relatively high
probability, while P("zxzxzxzyyy") would be near zero.

P(w|c), the probability that w would be typed in a text when the author meant c. This is the error model: think of it
 as answering "how likely is it that the author would type w by mistake when c was intended?"

argmaxc, the control mechanism, which says to enumerate all feasible values of c, and then choose the one that gives the best combined probability score
'''


# returns all words in the parameter 'text'
def words(text):

    return re.findall('[a-z]+', text.lower())


# simply count the frequency of each word in or training set
def train(features):

    # default value of 1 in order to smooth the function
    model = collections.defaultdict(lambda: 1)

    for feature in features:

        model[feature] += 1

    return model


NWORDS = train(words(file('big.txt').read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

keyboard = [['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            ['z', 'x', 'c', 'v', 'b', 'n', 'm']]


# this will return all possible words with an edit distance of 1.
def edits1(word):

    # split the word into two sections, left side and right side
    s = [(word[:i], word[i:]) for i in range(len(word) + 1)]

    # create a new set which deletes a single letter from the word
    deletes = [a + b[1:] for a, b in s if b]

    # swap two letter that are next to each other
    transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b) > 1]

    # replace every letter with every other possible letter
    replaces = [a + c + b[1:] for a, b in s for c in alphabet if b]

    # insert a new letter in every possible position
    inserts = [a + c + b for a, b in s for c in alphabet]

    # return the set of all possible words  ( possible words are not necessarily defined in the dictionary, instead the
    # possible words are just all possible combinations of letter sequences that follow the above heuristics.
    return set(deletes + transposes + replaces + inserts)


# return all possible words with an edit distance of 2.
def known_edits2(word):

    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)


# returns a set of known words
def known(words):

    return set(w for w in words if w in NWORDS)


# return the word that has the maximum frequency in the set of known words
def correct(word):

    # this will return the first set that contains a word. The order of this sequence should significantly impact
    # results which means it has the possibility to be optimized
    # known([word]) = maybe the word is not misspelled then don't correct it
    # known(edits1(word)) = maybe the word is slightly misspelled, being off by only a single "edit distance"
    # known_edits2(word) = maybe the word is slightly more misspelled, being off by only an "edit distance" of 2
    # [word] = all else failed, maybe the word is correct and our system has never seen it before

    #candidates = known([word]).union(known(edits1(word))).union(known_edits2(word)).union([word])

    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]

    # return the word with the highest frequency in our dictionary
    return max(candidates, key=NWORDS.get)


# return a tuple containing the row and column index of the position of the letter relative to a keyboard
def get_letter_indices(letter):

    for row_index in range(len(keyboard)):

        for col_index in range(len(keyboard[row_index])):

            if letter == keyboard[row_index][col_index]:

                return row_index, col_index


################ Testing code from here on ################
def spelltest(tests, bias=None, verbose=False):

    import time

    n, bad, unknown, start = 0, 0, 0, time.clock()

    if bias:

        for target in tests:

            NWORDS[target] += bias

    for target, wrongs in tests.items():

        for wrong in wrongs.split():

            n += 1

            w = correct(wrong)

            if w != target:

                bad += 1

                unknown += (target not in NWORDS)

                if verbose:

                    print 'correct(%r) => %r (%d); expected %r (%d)' % \
                          (wrong, w, NWORDS[w], target, NWORDS[target])

    return dict(bad=bad, n=n, bias=bias, percent_correct=str(int(100. - 100.*bad/n))+'%', unknown=unknown, secs=int(time.clock()-start))

tests1 = {'access': 'acess', 'accessing': 'accesing', 'accommodation':
'accomodation acommodation acomodation', 'account': 'acount', 'address':
'adress adres', 'addressable': 'addresable', 'arranged': 'aranged arrainged',
'arrangeing': 'aranging', 'arrangement': 'arragment', 'articles': 'articals',
'aunt': 'annt anut arnt', 'auxiliary':  'auxillary', 'available': 'avaible',
'awful': 'awfall afful', 'basically': 'basicaly', 'beginning': 'begining',
'benefit': 'benifit', 'benefits': 'benifits', 'between': 'beetween', 'bicycle':
'bicycal bycicle bycycle', 'biscuits':
'biscits biscutes biscuts bisquits buiscits buiscuts', 'built': 'biult',
'cake': 'cak', 'career': 'carrer',
'cemetery': 'cemetary semetary', 'centrally': 'centraly', 'certain': 'cirtain',
'challenges': 'chalenges chalenges', 'chapter': 'chaper chaphter chaptur',
'choice': 'choise', 'choosing': 'chosing', 'clerical': 'clearical',
'committee': 'comittee', 'compare': 'compair', 'completely': 'completly',
'consider': 'concider', 'considerable': 'conciderable', 'contented':
'contenpted contende contended contentid', 'curtains':
'cartains certans courtens cuaritains curtans curtians curtions', 'decide': 'descide', 'decided':
'descided', 'definitely': 'definately difinately', 'definition': 'defenition',
'definitions': 'defenitions', 'description': 'discription', 'desiccate':
'desicate dessicate dessiccate', 'diagrammatically': 'diagrammaticaally',
'different': 'diffrent', 'driven': 'dirven', 'ecstasy': 'exstacy ecstacy',
'embarrass': 'embaras embarass', 'establishing': 'astablishing establising',
'experience': 'experance experiance', 'experiences': 'experances', 'extended':
'extented', 'extremely': 'extreamly', 'fails': 'failes', 'families': 'familes',
'february': 'febuary', 'further': 'futher', 'gallery': 'galery gallary gallerry gallrey',
'hierarchal': 'hierachial', 'hierarchy': 'hierchy', 'inconvenient':
'inconvienient inconvient inconvinient', 'independent': 'independant independant',
'initial': 'intial', 'initials': 'inetials inistals initails initals intials',
'juice': 'guic juce jucie juise juse', 'latest': 'lates latets latiest latist',
'laugh': 'lagh lauf laught lugh', 'level': 'leval',
'levels': 'levals', 'liaison': 'liaision liason', 'lieu': 'liew', 'literature':
'litriture', 'loans': 'lones', 'locally': 'localy', 'magnificent':
'magnificnet magificent magnifcent magnifecent magnifiscant magnifisent magnificant',
'management': 'managment', 'meant': 'ment', 'minuscule': 'miniscule',
'minutes': 'muinets', 'monitoring': 'monitering', 'necessary':
'neccesary necesary neccesary necassary necassery neccasary', 'occurrence':
'occurence occurence', 'often': 'ofen offen offten ofton', 'opposite':
'opisite oppasite oppesite oppisit oppisite opposit oppossite oppossitte', 'parallel':
'paralel paralell parrallel parralell parrallell', 'particular': 'particulaur',
'perhaps': 'perhapse', 'personnel': 'personnell', 'planned': 'planed', 'poem':
'poame', 'poems': 'poims pomes', 'poetry': 'poartry poertry poetre poety powetry',
'position': 'possition', 'possible': 'possable', 'pretend':
'pertend protend prtend pritend', 'problem': 'problam proble promblem proplen',
'pronunciation': 'pronounciation', 'purple': 'perple perpul poarple',
'questionnaire': 'questionaire', 'really': 'realy relley relly', 'receipt':
'receit receite reciet recipt', 'receive': 'recieve', 'refreshment':
'reafreshment refreshmant refresment refressmunt', 'remember': 'rember remeber rememmer rermember',
'remind': 'remine remined', 'scarcely': 'scarcly scarecly scarely scarsely',
'scissors': 'scisors sissors', 'separate': 'seperate',
'singular': 'singulaur', 'someone': 'somone', 'sources': 'sorces', 'southern':
'southen', 'special': 'speaical specail specal speical', 'splendid':
'spledid splended splened splended', 'standardizing': 'stanerdizing', 'stomach':
'stomac stomache stomec stumache', 'supersede': 'supercede superceed', 'there': 'ther',
'totally': 'totaly', 'transferred': 'transfred', 'transportability':
'transportibility', 'triangular': 'triangulaur', 'understand': 'undersand undistand',
'unexpected': 'unexpcted unexpeted unexspected', 'unfortunately':
'unfortunatly', 'unique': 'uneque', 'useful': 'usefull', 'valuable': 'valubale valuble',
'variable': 'varable', 'variant': 'vairiant', 'various': 'vairious',
'visited': 'fisited viseted vistid vistied', 'visitors': 'vistors',
'voluntary': 'volantry', 'voting': 'voteing', 'wanted': 'wantid wonted',
'whether': 'wether', 'wrote': 'rote wote'}

tests2 = {'forbidden': 'forbiden', 'decisions': 'deciscions descisions',
'supposedly': 'supposidly', 'embellishing': 'embelishing', 'technique':
'tecnique', 'permanently': 'perminantly', 'confirmation': 'confermation',
'appointment': 'appoitment', 'progression': 'progresion', 'accompanying':
'acompaning', 'applicable': 'aplicable', 'regained': 'regined', 'guidelines':
'guidlines', 'surrounding': 'serounding', 'titles': 'tittles', 'unavailable':
'unavailble', 'advantageous': 'advantageos', 'brief': 'brif', 'appeal':
'apeal', 'consisting': 'consisiting', 'clerk': 'cleark clerck', 'component':
'componant', 'favourable': 'faverable', 'separation': 'seperation', 'search':
'serch', 'receive': 'recieve', 'employees': 'emploies', 'prior': 'piror',
'resulting': 'reulting', 'suggestion': 'sugestion', 'opinion': 'oppinion',
'cancellation': 'cancelation', 'criticism': 'citisum', 'useful': 'usful',
'humour': 'humor', 'anomalies': 'anomolies', 'would': 'whould', 'doubt':
'doupt', 'examination': 'eximination', 'therefore': 'therefoe', 'recommend':
'recomend', 'separated': 'seperated', 'successful': 'sucssuful succesful',
'apparent': 'apparant', 'occurred': 'occureed', 'particular': 'paerticulaur',
'pivoting': 'pivting', 'announcing': 'anouncing', 'challenge': 'chalange',
'arrangements': 'araingements', 'proportions': 'proprtions', 'organized':
'oranised', 'accept': 'acept', 'dependence': 'dependance', 'unequalled':
'unequaled', 'numbers': 'numbuers', 'sense': 'sence', 'conversely':
'conversly', 'provide': 'provid', 'arrangement': 'arrangment',
'responsibilities': 'responsiblities', 'fourth': 'forth', 'ordinary':
'ordenary', 'description': 'desription descvription desacription',
'inconceivable': 'inconcievable', 'data': 'dsata', 'register': 'rgister',
'supervision': 'supervison', 'encompassing': 'encompasing', 'negligible':
'negligable', 'allow': 'alow', 'operations': 'operatins', 'executed':
'executted', 'interpretation': 'interpritation', 'hierarchy': 'heiarky',
'indeed': 'indead', 'years': 'yesars', 'through': 'throut', 'committee':
'committe', 'inquiries': 'equiries', 'before': 'befor', 'continued':
'contuned', 'permanent': 'perminant', 'choose': 'chose', 'virtually':
'vertually', 'correspondence': 'correspondance', 'eventually': 'eventully',
'lonely': 'lonley', 'profession': 'preffeson', 'they': 'thay', 'now': 'noe',
'desperately': 'despratly', 'university': 'unversity', 'adjournment':
'adjurnment', 'possibilities': 'possablities', 'stopped': 'stoped', 'mean':
'meen', 'weighted': 'wagted', 'adequately': 'adequattly', 'shown': 'hown',
'matrix': 'matriiix', 'profit': 'proffit', 'encourage': 'encorage', 'collate':
'colate', 'disaggregate': 'disaggreagte disaggreaget', 'receiving':
'recieving reciving', 'proviso': 'provisoe', 'umbrella': 'umberalla', 'approached':
'aproached', 'pleasant': 'plesent', 'difficulty': 'dificulty', 'appointments':
'apointments', 'base': 'basse', 'conditioning': 'conditining', 'earliest':
'earlyest', 'beginning': 'begining', 'universally': 'universaly',
'unresolved': 'unresloved', 'length': 'lengh', 'exponentially':
'exponentualy', 'utilized': 'utalised', 'set': 'et', 'surveys': 'servays',
'families': 'familys', 'system': 'sysem', 'approximately': 'aproximatly',
'their': 'ther', 'scheme': 'scheem', 'speaking': 'speeking', 'repetitive':
'repetative', 'inefficient': 'ineffiect', 'geneva': 'geniva', 'exactly':
'exsactly', 'immediate': 'imediate', 'appreciation': 'apreciation', 'luckily':
'luckeley', 'eliminated': 'elimiated', 'believe': 'belive', 'appreciated':
'apreciated', 'readjusted': 'reajusted', 'were': 'wer where', 'feeling':
'fealing', 'and': 'anf', 'false': 'faulse', 'seen': 'seeen', 'interrogating':
'interogationg', 'academically': 'academicly', 'relatively': 'relativly relitivly',
'traditionally': 'traditionaly', 'studying': 'studing',
'majority': 'majorty', 'build': 'biuld', 'aggravating': 'agravating',
'transactions': 'trasactions', 'arguing': 'aurguing', 'sheets': 'sheertes',
'successive': 'sucsesive sucessive', 'segment': 'segemnt', 'especially':
'especaily', 'later': 'latter', 'senior': 'sienior', 'dragged': 'draged',
'atmosphere': 'atmospher', 'drastically': 'drasticaly', 'particularly':
'particulary', 'visitor': 'vistor', 'session': 'sesion', 'continually':
'contually', 'availability': 'avaiblity', 'busy': 'buisy', 'parameters':
'perametres', 'surroundings': 'suroundings seroundings', 'employed':
'emploied', 'adequate': 'adiquate', 'handle': 'handel', 'means': 'meens',
'familiar': 'familer', 'between': 'beeteen', 'overall': 'overal', 'timing':
'timeing', 'committees': 'comittees commitees', 'queries': 'quies',
'econometric': 'economtric', 'erroneous': 'errounous', 'decides': 'descides',
'reference': 'refereence refference', 'intelligence': 'inteligence',
'edition': 'ediion ediition', 'are': 'arte', 'apologies': 'appologies',
'thermawear': 'thermawere thermawhere', 'techniques': 'tecniques',
'voluntary': 'volantary', 'subsequent': 'subsequant subsiquent', 'currently':
'curruntly', 'forecast': 'forcast', 'weapons': 'wepons', 'routine': 'rouint',
'neither': 'niether', 'approach': 'aproach', 'available': 'availble',
'recently': 'reciently', 'ability': 'ablity', 'nature': 'natior',
'commercial': 'comersial', 'agencies': 'agences', 'however': 'howeverr',
'suggested': 'sugested', 'career': 'carear', 'many': 'mony', 'annual':
'anual', 'according': 'acording', 'receives': 'recives recieves',
'interesting': 'intresting', 'expense': 'expence', 'relevant':
'relavent relevaant', 'table': 'tasble', 'throughout': 'throuout', 'conference':
'conferance', 'sensible': 'sensable', 'described': 'discribed describd',
'union': 'unioun', 'interest': 'intrest', 'flexible': 'flexable', 'refered':
'reffered', 'controlled': 'controled', 'sufficient': 'suficient',
'dissension': 'desention', 'adaptable': 'adabtable', 'representative':
'representitive', 'irrelevant': 'irrelavent', 'unnecessarily': 'unessasarily',
'applied': 'upplied', 'apologised': 'appologised', 'these': 'thees thess',
'choices': 'choises', 'will': 'wil', 'procedure': 'proceduer', 'shortened':
'shortend', 'manually': 'manualy', 'disappointing': 'dissapoiting',
'excessively': 'exessively', 'comments': 'coments', 'containing': 'containg',
'develop': 'develope', 'credit': 'creadit', 'government': 'goverment',
'acquaintances': 'aquantences', 'orientated': 'orentated', 'widely': 'widly',
'advise': 'advice', 'difficult': 'dificult', 'investigated': 'investegated',
'bonus': 'bonas', 'conceived': 'concieved', 'nationally': 'nationaly',
'compared': 'comppared compased', 'moving': 'moveing', 'necessity':
'nessesity', 'opportunity': 'oppertunity oppotunity opperttunity', 'thoughts':
'thorts', 'equalled': 'equaled', 'variety': 'variatry', 'analysis':
'analiss analsis analisis', 'patterns': 'pattarns', 'qualities': 'quaties', 'easily':
'easyly', 'organization': 'oranisation oragnisation', 'the': 'thw hte thi',
'corporate': 'corparate', 'composed': 'compossed', 'enormously': 'enomosly',
'financially': 'financialy', 'functionally': 'functionaly', 'discipline':
'disiplin', 'announcement': 'anouncement', 'progresses': 'progressess',
'except': 'excxept', 'recommending': 'recomending', 'mathematically':
'mathematicaly', 'source': 'sorce', 'combine': 'comibine', 'input': 'inut',
'careers': 'currers carrers', 'resolved': 'resoved', 'demands': 'diemands',
'unequivocally': 'unequivocaly', 'suffering': 'suufering', 'immediately':
'imidatly imediatly', 'accepted': 'acepted', 'projects': 'projeccts',
'necessary': 'necasery nessasary nessisary neccassary', 'journalism':
'journaism', 'unnecessary': 'unessessay', 'night': 'nite', 'output':
'oputput', 'security': 'seurity', 'essential': 'esential', 'beneficial':
'benificial benficial', 'explaining': 'explaning', 'supplementary':
'suplementary', 'questionnaire': 'questionare', 'employment': 'empolyment',
'proceeding': 'proceding', 'decision': 'descisions descision', 'per': 'pere',
'discretion': 'discresion', 'reaching': 'reching', 'analysed': 'analised',
'expansion': 'expanion', 'although': 'athough', 'subtract': 'subtrcat',
'analysing': 'aalysing', 'comparison': 'comparrison', 'months': 'monthes',
'hierarchal': 'hierachial', 'misleading': 'missleading', 'commit': 'comit',
'auguments': 'aurgument', 'within': 'withing', 'obtaining': 'optaning',
'accounts': 'acounts', 'primarily': 'pimarily', 'operator': 'opertor',
'accumulated': 'acumulated', 'extremely': 'extreemly', 'there': 'thear',
'summarys': 'sumarys', 'analyse': 'analiss', 'understandable':
'understadable', 'safeguard': 'safegaurd', 'consist': 'consisit',
'declarations': 'declaratrions', 'minutes': 'muinutes muiuets', 'associated':
'assosiated', 'accessibility': 'accessability', 'examine': 'examin',
'surveying': 'servaying', 'politics': 'polatics', 'annoying': 'anoying',
'again': 'agiin', 'assessing': 'accesing', 'ideally': 'idealy', 'scrutinized':
'scrutiniesed', 'simular': 'similar', 'personnel': 'personel', 'whereas':
'wheras', 'when': 'whn', 'geographically': 'goegraphicaly', 'gaining':
'ganing', 'requested': 'rquested', 'separate': 'seporate', 'students':
'studens', 'prepared': 'prepaired', 'generated': 'generataed', 'graphically':
'graphicaly', 'suited': 'suted', 'variable': 'varible vaiable', 'building':
'biulding', 'required': 'reequired', 'necessitates': 'nessisitates',
'together': 'togehter', 'profits': 'proffits'}


if __name__ == '__main__':
    print spelltest(tests1)



