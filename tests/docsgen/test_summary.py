from docsgen.summary import WB_PORTAL, clean_summary


def test_unescapes_quotes_from_rust_doc_comments():
    assert clean_summary('Метод \\"быстрый\\"') == 'Метод "быстрый"'


def test_strips_html_but_keeps_its_text():
    text = '<div class="description_token"> Метод <strong>доступен</strong> по токену </div>'
    assert clean_summary(text) == "Метод доступен по токену"


def test_rewrites_root_relative_markdown_links_to_the_portal():
    text = "Удаляет ярлык из [списка](/openapi/item-management#tag/labels) продавца."
    assert clean_summary(text) == (
        "Удаляет ярлык из [списка]"
        f"({WB_PORTAL}/openapi/item-management#tag/labels) продавца."
    )


def test_rewrites_root_relative_html_links_before_stripping_tags():
    text = 'Метод <a href="/openapi/api-information#tag/auth">доступен</a> по токену'
    assert clean_summary(text) == "Метод доступен по токену"


def test_leaves_absolute_links_alone():
    text = "Описание со ссылкой на [портал](https://dev.wildberries.ru/openapi/api-information)."
    assert clean_summary(text) == text


def test_collapses_whitespace_and_newlines():
    assert clean_summary("Метод  удаляет\n\n  ярлык") == "Метод удаляет ярлык"


def test_cuts_at_the_first_sentence_when_the_text_runs_long():
    text = "Короткое предложение. " + "Длинный хвост с лимитами. " * 20
    assert clean_summary(text) == "Короткое предложение."


def test_truncates_a_long_sentence_with_an_ellipsis():
    text = "Слово " * 100
    out = clean_summary(text)
    assert len(out) <= 201
    assert out.endswith("…")


def test_never_truncates_inside_a_markdown_link():
    text = "а" * 190 + " [подробнее](/openapi/item-management#tag/labels) далее"
    out = clean_summary(text)
    assert out.count("[") == out.count("](") == out.count(")")
    assert "/openapi" not in out or out.endswith(")")


def test_tables_are_dropped_with_the_tail():
    text = ("Метод удаляет ярлык. | Тип | Период | Лимит | | --- | --- | --- | "
            "| Персональный | 1 минута | 100 |")
    assert clean_summary(text) == "Метод удаляет ярлык."


def test_empty_input_stays_empty():
    assert clean_summary("") == ""
    assert clean_summary("   <div>  </div> ") == ""


def test_drops_the_styled_badge_blocks_wb_puts_in_front():
    text = ('<div class="description_token"> Метод <a href="/openapi/x">доступен</a> по '
            '<strong>Персональному</strong> токену </div>  Метод удаляет пользователя.')
    assert clean_summary(text) == "Метод удаляет пользователя."


def test_keeps_the_badge_text_when_it_is_the_whole_description():
    text = '<div class="description_limit"> Лимит 100 запросов в минуту </div>'
    assert clean_summary(text) == "Лимит 100 запросов в минуту"
