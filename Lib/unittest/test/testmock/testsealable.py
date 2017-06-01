import unittest
from unittest import mock


class SampleObject(object):
    def __init__(self):
        self.attr_sample1 = 1
        self.attr_sample2 = 1

    def method_sample1(self):
        pass

    def method_sample2(self):
        pass


class TestSealable(unittest.TestCase):
    """Validates the ability to seal a mock which freezes its spec"""

    def test_attributes_return_more_mocks_by_default(self):
        m = mock.Mock()

        assert isinstance(m.test, mock.Mock)
        assert isinstance(m.test(), mock.Mock)
        assert isinstance(m.test().test2(), mock.Mock)


    def test_new_attributes_cannot_be_accessed_on_seal(self):
        m = mock.Mock()

        mock.seal(m)
        with self.assertRaises(AttributeError):
            m.test
        with self.assertRaises(AttributeError):
            m()


    def test_new_attributes_cannot_be_set_on_seal(self):
        m = mock.Mock()

        mock.seal(m)
        with self.assertRaises(AttributeError):
            m.test = 1


    def test_existing_attributes_allowed_after_seal(self):
        m = mock.Mock()

        m.test.return_value = 3

        mock.seal(m)
        assert m.test() == 3


    def test_initialized_attributes_allowed_after_seal(self):
        m = mock.Mock(test_value=1)

        mock.seal(m)
        assert m.test_value == 1


    def test_call_on_sealed_mock_fails(self):
        m = mock.Mock()

        mock.seal(m)
        with self.assertRaises(AttributeError):
            m()


    def test_call_on_defined_sealed_mock_succeeds(self):
        m = mock.Mock(return_value=5)

        mock.seal(m)
        assert m() == 5


    def test_seals_recurse_on_added_attributes(self):
        m = mock.Mock()

        m.test1.test2().test3 = 4

        mock.seal(m)
        assert m.test1.test2().test3 == 4
        with self.assertRaises(AttributeError):
            m.test1.test2.test4


    def test_seals_dont_recurse_on_manual_attributes(self):
        m = mock.Mock(name="root_mock")

        m.test1.test2 = mock.Mock(name="not_sealed")
        m.test1.test2.test3= 4

        mock.seal(m)
        assert m.test1.test2.test3 == 4
        m.test1.test2.test4  # Does not raise
        m.test1.test2.test4 = 1  # Does not raise


    def test_integration_with_spec_att_definition(self):
        """You are not restricted when defining attributes on a mock with spec"""
        m = mock.Mock(SampleObject)

        m.attr_sample1 = 1
        m.attr_sample3 = 3

        mock.seal(m)
        assert m.attr_sample1 == 1
        assert m.attr_sample3 == 3
        with self.assertRaises(AttributeError):
            m.attr_sample2


    def test_integration_with_spec_method_definition(self):
        """You need to defin the methods, even if they are in the spec"""
        m = mock.Mock(SampleObject)

        m.method_sample1.return_value = 1

        mock.seal(m)
        assert m.method_sample1() == 1
        with self.assertRaises(AttributeError):
            m.method_sample2()


    def test_integration_with_spec_method_definition_respects_spec(self):
        """You cannot define methods out of the spec"""
        m = mock.Mock(SampleObject)

        with self.assertRaises(AttributeError):
            m.method_sample3.return_value = 3


    def test_sealed_exception_has_attribute_name(self):
        m = mock.Mock()

        mock.seal(m)
        try:
            m.SECRETE_name
        except AttributeError as ex:
            assert "SECRETE_name" in str(ex)

    def test_attribute_chain_is_maintained(self):
        m = mock.Mock(name="mock_name")
        m.test1.test2.test3.test4

        mock.seal(m)
        try:
            m.test1.test2.test3.test4.boom
        except AttributeError as ex:
            assert "mock_name.test1.test2.test3.test4.boom" in str(ex)

    def test_call_chain_is_maintained(self):
        m = mock.Mock()
        m.test1().test2.test3().test4

        mock.seal(m)
        try:
            m.test1().test2.test3().test4()
        except AttributeError as ex:
            assert "mock.test1().test2.test3().test4" in str(ex)

if __name__ == "__main__":
    unittest.main()
