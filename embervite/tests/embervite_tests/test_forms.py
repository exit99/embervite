from embervite.forms import pop_form_kwarg


def test_pop_form_kwarg():
    kwargs = {'test': 1, 'ing': 2}
    item, new_kwargs = pop_form_kwarg('ing', kwargs)
    assert item == 2
    assert 'ing' not in new_kwargs.keys()
    assert 'ing' not in kwargs.keys()
