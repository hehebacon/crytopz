from language_manager import lang


print(
    lang.t("settings")
)


lang.change("en")


print(
    lang.t("settings")
)