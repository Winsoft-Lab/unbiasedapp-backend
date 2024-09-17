import pandas


def sorter(text: list, delimiter="", use_regex=False):
    """_summary_

    Args:
        text (list): _description_
        delimiter (str, optional): _description_. Defaults to "".
        use_regex (bool, optional): _description_. Defaults to False.

    Returns:
        pandas.DataFrame: _description_
    """
    import numpy as np

    val = []

    if use_regex:
        import re

        datepatern = re.compile(r"\d+-\d+-\d+")
        for text in text:
            date = datepatern.findall(text)
            txt = datepatern.sub(" ", text)
            if len(date) != 0:
                _ = date[0]
            else:
                _ = None

            val.append((f"{_}", txt))

    for text in text:
        txt_date = text.split(delimiter)
        if len(txt_date) > 1:
            print(txt_date)
            txt = txt_date[0]
            date = txt_date[1]
        else:
            pass
        val.append((f"{date}", txt))

    result = np.array(val)

    import pandas as pd

    df = pd.DataFrame(result, columns=["DATE", "TEXT"])

    # print(df)

    return df


# d = [
#     "4 out of 5Its coolNice product10-10-2022by JuliusVerified Purchase",
#     "5 out of 5it's very portableI like the product because it really sounds well04-10-2022by DavidVerified Purchase",
#     "5 out of 5Neat soundNoiseless when on but not in use. The sound is worth the price04-10-2022by Jason AkhuemokhanVerified Purchase",
#     "4 out of 5Its okaySmall but mighty30-09-2022by ADESOJI JOSHUAVerified Purchase",
#     "3 out of 5Power on/offIt could have been better if it has remote control for power on/off29-09-2022by AnthonyVerified Purchase",
#     "5 out of 5The reviews don't lieMatches the description perfectly... you need to hear the bass though, good God!!29-09-2022by BaronnayaVerified Purchase",
#     "5 out of 5It's amazingAn example of money well spent29-09-2022by Mr DanVerified Purchase",
#     "5 out of 5The reviwI love the sound especially the base, love it♥️28-09-2022by AjetunmobiVerified Purchase",
#     "5 out of 5I love itAwesome ????27-09-2022by DomaVerified Purchase",
#     "5 out of 5More than like itThe speaker is a perfect description of small but mightiest. Sound system like no other. Thank God I got it.27-09-2022by TOLULOPEVerified Purchase",
#     "5 out of 5I like it100% recommended26-09-2022by MuhammadVerified Purchase",
#     "5 out of 5This is an incredibly powerful boxThe fact that it's small but produces mighty sound get me everytime. I want to believe there is a reason why a remote isn't added I feel it would increase the cost of it.",
#     "It is a very nice thing to have.26-09-2022by OluwalosolaeyiVerified Purchase",
#     "5 out of 5Well it's worth the priceI'm glad I got it, I've been longing for it for a very long time.26-09-2022by XaviourVerified Purchase",
#     "5 out of 5Excellent productThe device works better than its price. The bass was actually so better than I thought it would be26-09-2022by AlabaVerified Purchase",
#     "5 out of 5Small but mightyVery very nice23-09-2022by EGONUVerified Purchase",
#     "4 out of 5SuperbInitially I underrated this product but it really beat my expectations . It's small and mighty . I totally recommend .21-09-2022by EmmanuelVerified Purchase",
#     "5 out of 5LoveSolid buy!21-09-2022by JohnVerified Purchase",
#     "4 out of 5I like it for it's money and the type of productIt's cool I hope it's serve well in the future21-09-2022by AdewaleVerified Purchase",
#     "4 out of 5Nice pieceProduce good sound20-09-2022by Aaron TankoVerified Purchase",
#     "5 out of 5I love itJust giving me the sounds I want20-09-2022by OlaoluVerified Purchase",
#     "5 out of 5I love this productIt works well and amplifies sound well.20-09-2022by PaulVerified Purchase",
#     "5 out of 5I like itSo good for the price it gives the sounds needed and it’s very Suitable for home20-09-2022by MathewreyVerified Purchase",
#     "5 out of 5AwesomeThis product beat my imagination.............. Am still in shock at the sound production.....",
#     "Just what i want20-09-2022by SamuelVerified Purchase",
#     "5 out of 5I like itSound very good19-09-2022by MuhammedVerified Purchase",
#     "4 out of 5its coolIts smaller in size but, good sound, its for shop anyway, so am cool with it19-09-2022by EMMANUELVerified Purchase",
#     "4 out of 5i like itgood product16-09-2022by NgulubeVerified Purchase",
#     "5 out of 5Love itBetter than my expectations... Great sound output13-09-2022by SamuelVerified Purchase",
#     "5 out of 5The soundIt's good in quality and best when it comes to music... It's super in product ❤️13-09-2022by ElkanahVerified Purchase",
#     "5 out of 5GoodUseful13-09-2022by OffonzVerified Purchase",
#     "5 out of 5I like itI got real value for my money. It exceeded my expectation, hence I'm giving it 5 stars12-09-2022by NUMOVerified Purchase",
#     "4 out of 5Very good and beautifulIt okay and very easy to connect, i wonder why many comment i read b4 buying this says it not connecting to thier tv. 2. I gave it 4 stars because it need remote and the volume should be increase. Its okay for indoor use only as indicated. Small, mighty n portable thank God my hubby like my choice.21-07-2022by MorenikeVerified Purchase",
#     "4 out of 5Very good and beautifulIt okay and very easy to connect, i wonder why many comment i read b4 buying this says it not connecting to thier tv. 2. I gave it 4 stars because it need remote and the volume should be increase. Its okay for indoor use only as indicated. Small, mighty n portable thank God my hubby like my choice.21-07-2022by MorenikeVerified Purchase",
#     "5 out of 5Edifier multimedia speakersI love this product so much. This is actually the second I'm getting cause the first I bought is serving me well at home so I got a second for my studio. It's perfect. Light weight and very portable with a perfect sound system21-07-2022by PattyVerified Purchase",
#     "5 out of 5Amazing sound at a budget priceHad my doubts about it till I bought it and now I'm really glad I did. I don't think you can get a better deal for a sound system at this price20-07-2022by MinkababzVerified Purchase",
#     "4 out of 5Good ProductVery good for the price. I connected it on my DStv decoder and I love it. Though it more louder when connected on Bluetooth. For those finding it difficult to connect to decoder/tv please watch the video online see how you can navigate your way through. ",
#     "I would have given it a 5 ???? but the volume is a no for me.",
#     "I recommend for those on a very tight budget.19-07-2022by ProsperVerified Purchase",
#     "5 out of 5I Like itGood sound quality19-07-2022by SheriffVerified Purchase",
#     "4 out of 5I like itIt's okay as prescribed.19-07-2022by Abdul-azeezVerified Purchase",
#     "5 out of 5is amazingThe bass is okay19-07-2022by oziomaVerified Purchase",
#     "5 out of 5I like itlovely sound for an enclosed place. Worth the buy.19-07-2022by GloriaVerified Purchase",
#     "5 out of 5i like itDe bazz is ok + volume just that u can't connect it to a TV18-07-2022by JeremiahVerified Purchase",
#     "5 out of 5I like itVery Good31-07-2021by OladayoVerified Purchase",
#     "5 out of 5I like itIt’s awesome30-07-2021by oluwaferanmiVerified Purchase",
#     "5 out of 5Awesome!Good sound it's all perfect for me it's fine.♥️♥️♥️♥️♥️26-07-2021by PaulVerified Purchase",
#     "4 out of 5Not BadThe sound quality is fair with the price, the only drawback is that it does not have a remote control. I find it a little difficult adjusting the volume etc without a remote control. Everything about it is just manually operated. It still beat many others within the price range in sound quality.22-07-2021by CHRISTIANVerified Purchase",
#     "1 out of 5I don't like itThe bass is horrible ",
#     "I regret buying it19-07-2021by HarrisonVerified Purchase",
#     "5 out of 5Good soundSound is great love it19-07-2021by LAWRENCE IKENNAVerified Purchase",
#     "5 out of 5I love itThe output is so madt plus bass is so on point... But I would've loved if it came with a remote control... ????18-07-2021by JoshuaVerified Purchase",
#     "5 out of 5I love it.It's superb.16-07-2021by MahmudVerified Purchase",
#     "4 out of 5I like itThe product is okay16-07-2021by ISOLARVerified Purchase",
#     "5 out of 5like itblasting it as I type, love it15-07-2021by JonasVerified Purchase",
#     "4 out of 5like itthe sound production quality is very good04-07-2021by UGWUVerified Purchase",
#     "5 out of 5I love itIt's a really cool sound system.02-07-2021by AyomideVerified Purchase",
#     "5 out of 5I like itIt's a good one, I love it01-07-2021by HammedVerified Purchase",
#     "5 out of 5AWESOMEGreat sound, and easy to use.30-06-2021by RAPHAELVerified Purchase",
#     "5 out of 5GOOD PRODUCTSound amazing28-06-2021by OLUWAGBEMIGAVerified Purchase",
#     "5 out of 5very okayGood product20-05-2021by OlawumiVerified Purchase",
#     "4 out of 5okIs ok but they should improve on the bass09-05-2021by NWAOKETEVerified Purchase",
# ]
# d = [
#     "Great phone and affordable.>May 13, 2022",
#     "Durable product>September 2, 2022",
#     "Good product >July 31, 2022",
#     "good product>May 13, 2022",
#     "love this is why i am ordering another one right now>August 15, 2022",
#     "okay>June 13, 2022",
#     "Good phone for normal tasks, and cool infinity lcd too.>May 11, 2022",
#     "Working perfectly well, Konga are too good in delivery agent.>June 9, 2022",
#     "The best product, great connectivity durable battery and clear cameras>July 7, 2022",
#     "Lovely >May 12, 2022",
#     "great>May 26, 2022",
#     "Good product>May 28, 2022",
#     "",
# ]

# new = sorter(d, delimiter=">")

# import pandas as pd

# df = pd.DataFrame(new, columns=["DATE", "TEXT"])
# print(df)
