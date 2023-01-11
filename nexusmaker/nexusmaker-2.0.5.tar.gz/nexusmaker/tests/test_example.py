from nexusmaker import NexusMaker, Record

# language      cognate             = nexus
# Maori    		1                   = 10
# Maori    	 	<not cognate>       = // removed as already coded for word
# Samoan 		1                   = 10
# Tahiatian  	<not cognate>       = u1
# Tahiatian  	<not cognate>       = // removed as already coded for word
# Tahiatian  	<not cognate>       = // removed as already coded for word
# Tongan    	<no data>           = ??  // missing data


def test_example():
    maker = NexusMaker(data=[
        Record(ID=1, Language="Maori", Parameter="word1", Item="", Cognacy="1"),
        Record(ID=2, Language="Maori", Parameter="word1", Item="", Cognacy=""),
        Record(ID=3, Language="Samoan", Parameter="word1", Item="", Cognacy="1"),
        Record(ID=4, Language="Tahitian", Parameter="word1", Item="", Cognacy=""),
        Record(ID=5, Language="Tahitian", Parameter="word1", Item="", Cognacy=""),
        Record(ID=6, Language="Tahitian", Parameter="word1", Item="", Cognacy=""),
        # ...note missing Tongan entry here.

        # add some entries for word 2 so Tongan will show as missing
        Record(ID=7, Language="Tongan", Parameter="word2", Item="", Cognacy="1"),

    ])

    assert ('word1', '1') in maker.cognates
    assert ('word2', '1') in maker.cognates

    uniques = [
        c for c in maker.cognates
        if c[0] == 'word1'
        and c[1].startswith('u_')
    ]
    assert len(uniques) == 1
    assert sorted(maker.cognates[('word1', '1')]) == ['Maori', 'Samoan']
    assert sorted(maker.cognates[uniques[0]]) == ['Tahitian']
    assert sorted(maker.cognates[('word2', '1')]) == ['Tongan']

    assert maker._is_missing_for_parameter('Tongan', 'word1')

    nex = maker.make()
    assert nex.data['word1_1'] == {
        'Maori':    '1',
        'Samoan':   '1',
        'Tahitian': '0',
        'Tongan':   '?',
    }

    assert nex.data["_".join(uniques[0])] == {
        'Maori':    '0',
        'Samoan':   '0',
        'Tahitian': '1',
        'Tongan':   '?',
    }

    assert nex.data['word2_1'] == {
        'Maori':    '?',
        'Samoan':   '?',
        'Tahitian': '?',
        'Tongan':   '1',
    }
