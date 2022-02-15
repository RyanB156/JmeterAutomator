import re


def regex_test():
    script_texts = [
        '<stringProp name="HTTPSampler.domain">solver03.honeywellsaas.com</stringProp>',
        '<stringProp name="Header.value">https://solver03.honeywellsaas.com:7004/mas/connexo_login.html</stringProp>',
        '<stringProp name="HTTPSampler.domain">hic026732</stringProp>',
        '<stringProp name="Header.value">https://hic026732/mas/connexo_login.html</stringProp>'
    ]
    r = r'[\w.]+([:\d]+)? | '
    for s in script_texts:
        print(re.findall(r, s))

    # hic026732


if __name__ == '__main__':
    regex_test()