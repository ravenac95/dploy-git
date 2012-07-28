from mock import MagicMock, call


def failing_assertion_magic_mock():
    m = MagicMock()
    expected = []
    for i in range(5):
        expected.append(call(i))
        l = m.from_here(i)
        if l.branch == True:
            print "Should not get here"
    m.from_here.assert_has_calls(expected)


def failing_assertion_mock():
    m = MagicMock()
    expected = []
    for i in range(5):
        expected.append(call(i))
        l = m.from_here(i)
        if l.branch == True:
            print "Should not get here"
    m.from_here.assert_has_calls(expected)
