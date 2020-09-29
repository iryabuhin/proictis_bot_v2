import asyncio
from aiounittest import AsyncTestCase
from proictis_api.mentors import make_mentor_card


def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


class TestMentorCard:
    def test_card_photo_doc_link(self):
        card = _run(make_mentor_card('пленкин'))

        photo_link, doc_link = card[1:]

        assert photo_link == \
            'https://proictis.sfedu.ru/api/static/files/WhatsApp%20Image%202019-09-17%20at%20151122.5c7823b18bfd293bfb6ab31c-5d81e25bfc45d4693bd17e13.jpeg'

        assert doc_link == \
            r'https://proictis.sfedu.ru/api/static/files/Информация.5c7823b18bfd293bfb6ab31c-5c84bdea6739d504247c2ac2.pdf'

    def test_card_correct_text(self):
        actual_mentors = [
            "Федотова",
            "Пленкин",
            "Логощина",
            "Балабаев"
        ]

        cards = [_run(make_mentor_card(m)) for m in actual_mentors]

        assert cards[0][2].endswith('5c8668d92b1e9669706c1085.pdf')

        assert cards[1][2].endswith('5c84bdea6739d504247c2ac2.pdf')

        assert cards[2][2].endswith('5c9931d82b1e9669706c10da.pdf')

        assert cards[3][2].endswith('5df9d56a99f46d517c5fa2ac.pdf')

    def test_nonexistent_mentors(self):
        fake_surnames = [
            'Иванов',
            'Петров',
            'Дуров',
            'Николаев',
            'Александров',
            'Юров'
        ]
        for surname in fake_surnames:
            card = _run(make_mentor_card(surname))

            assert card is None


