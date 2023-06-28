from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd

OUTPUT_FILE_PATH = './etsy_data.csv'
DRIVER_PATH = 'C:/Git_Repo/Costco/costco-scrape/chrome_driver/new/chromedriver.exe'
MIN_PRICE = 'min'
MAX_PRICE = 'max'

class WebDriverLoadOverTimeException(Exception):
    pass


class PageNotFound(Exception):
    pass


def load_page(payload_url, web_driver):
    err_str = ''
    try:
        web_driver.get(payload_url)
    except TimeoutException as e:
        err_str += (str(e)) + ' | '
        try:
            web_driver.execute_script('''return window.stop''')
        except TimeoutException as e:
            err_str += (str(e)) + ' | '
            try:
                web_driver.get(payload_url)
            except Exception as e:
                err_str += (str(e)) + ' | '
                raise WebDriverLoadOverTimeException(err_str)


def extractBasicInformation(web_driver, page_url, **kwargs):
    try:
        load_page(page_url, web_driver)
        source_page = web_driver.page_source
        soup = BeautifulSoup(source_page, "html.parser")
        name = None
        try:
            name_element = soup.find('div', attrs={
                'class': 'img-container',
                'data-editable-img': 'user-avatar'
            })
            name = name_element.text.strip()
        except BaseException as e:
            print(f"Unable to extract name !!, error: {e}")

        print(f"Name: {name}")

        total_product = None
        try:
            total_product_btn = soup.find('button', attrs={
                                                    'class': 'wt-tab__item wt-ml-md-0 wt-mr-md-0 wt-justify-content-space-between is-selected',
                                                    'data-section-id': '0'
                                                    })
            total_product_elem = total_product_btn.find('span', class_='wt-mr-md-2')
            total_product = total_product_elem.text.strip()
        except BaseException as e:
            print(f"Unable to extract total product !!, error: {e}")

        print(f"Total product: {total_product}")

        return {'name': name, 'total_product': total_product}
    except BaseException as e:
        print(e)
        return dict()
    finally:
        web_driver.delete_all_cookies()


def extractFirstProductPrice(web_driver, page_url, price_type, **kwargs):
    try:
        load_page(page_url, web_driver)
        source_page = web_driver.page_source
        soup = BeautifulSoup(source_page, "html.parser")

        all_products_elem = soup.findAll('div',
                                         class_='js-merch-stash-check-listing v2-listing-card wt-position-relative wt-grid__item-xs-6 wt-flex-shrink-xs-1 wt-grid__item-xl-3 wt-grid__item-lg-4 wt-grid__item-md-4 listing-card-experimental-style')

        all_prices = set()
        for price_elem in all_products_elem:
            price = price_elem.find('span', class_='currency-value').text.strip()
            all_prices.add(float(price.replace(',', '')))

        if price_type == MIN_PRICE:
            all_prices = sorted(all_prices)
            print(f"Min price: {all_prices[0]}")
        else:
            all_prices = sorted(all_prices, reverse=True)
            print(f"Max price: {all_prices[0]}")

        return float(all_prices[0])
    except BaseException as e:
        print(e)
        return None
    finally:
        web_driver.delete_all_cookies()


def writeOutputToFile(output_data, output_file_path):
    try:
        print(f'Data to be written into the file: {output_data}')
        df = pd.DataFrame(output_data)
        df.to_csv(output_file_path, sep=',',  mode='a', encoding='utf-8', index=False, header=False)
        print('Output data written successfully...')
        return {
            'STATUS': 'SUCCESS',
            'DESCRIPTION': 'Successfully scrapped data ...'
        }
    except BaseException as e:
        print(f"Failed to write output into the file {output_file_path} !!, error: {e}")
        return {
            'STATUS': 'FAIL',
            'DESCRIPTION': f'Error: {e}'
        }


def process(web_driver=None, PID=None, **kwargs):
    try:
        url='https://www.etsy.com/shop/{}'.format(PID)
        basic_info = extractBasicInformation(web_driver, url)
        min_price = extractFirstProductPrice(web_driver, 'https://www.etsy.com/shop/{}?sort_order=price_asc'.format(PID), MIN_PRICE)
        max_price = extractFirstProductPrice(web_driver, 'https://www.etsy.com/shop/{}?sort_order=price_desc'.format(PID), MAX_PRICE)

        output_data = {
            'Name': [basic_info['name']],
            'Total Product': [basic_info['total_product']],
            'Min Price': [min_price],
            'Max Price': [max_price],
            'Price Range': [f'{min_price} - {max_price}'],
            'Price Average': [(min_price + max_price)/2 if min_price is not None and max_price is not None else None],
            'url':[url]
        }
        status = writeOutputToFile(output_data, OUTPUT_FILE_PATH)
        if status['STATUS'] == 'SUCCESS':
            status['PAYLOAD'] = output_data
            status['FILE_PATH'] = OUTPUT_FILE_PATH
        else:
            status['PAYLOAD'] = None
            status['FILE_PATH'] = None

        return status
    except (PageNotFound, Exception) as e:
        print(e)

        return {
            'STATUS': 'FAIL',
            'PAYLOAD': None,
            'FILE_PATH': None,
            'DESCRIPTION': f'Error: {e}'
        }


def initializeDriver():
    preferences = {"profile.managed_default_content_settings.images": 2}
    options = Options()
    options.add_experimental_option("prefs", preferences)

    web_driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)
    web_driver.set_page_load_timeout(15)
    web_driver.set_window_size(1024, 1440)

    return web_driver


def closeDriver(web_driver):
    web_driver.delete_all_cookies()
    web_driver.quit()


if __name__ == '__main__':
    driver = initializeDriver()
    list = ['CaitlynMinimalist', 'ModParty', 'Beadboat1', 'AcornandCrowStudio', 'HeatherRobertsArt', 'PersonalizationMall', 'SeedGeeks', 'DesignMyPartyStudio', 'SvgCafe', 'SouthernSeedExchange', 'DOMEDBAZAAR', 'PixelPerfectionParty', 'HappyKawaiiSupplies', 'EverlyGrayce', 'SEEDVILLEUSA', 'MignonandMignon', 'SweetytreatyCo', 'SilverRainSilver', 'geopersonalized', 'UnmeasuredEvent', 'WoodByStu', 'SilverPost', 'PrincessBeadSupply', 'Worldincensestore', 'elevado', 'CrcbeadsShop', 'BlingeeThingee', 'BABEINA', 'AZsupplies', 'MyPorchPrints', 'EmmePrintCo', 'TumblersPlanet', 'PartyTouchesUK', 'ZellajakeFarmGarden', 'KJewelryMetal', 'Spoonflower', 'TwistStationery', 'DreamworkshopCo', 'shoteanx', 'AWildBloomPrintables', 'CandieCooper', 'AfterLunaStudio', 'stonesdirect', 'MarryMePaperBoutique', 'WarungBeads', 'KatherineDream', 'JLDreamWorks', 'CitraGraphics', 'DigitalCurio', 'SewSweetParadise', 'CNDesignerDips', 'SHEMISLI', 'SvgMode', 'PaddingPaws', 'TumblersWithMelissa', 'YourWeddingPlace', 'LilMeStore', 'IsobelJadeDesigns', 'CowhideDigitalArt', 'MintyPaperieShop', 'MelaninSecret', 'MrRui', 'stitchinghousewives', 'DesignInYourHeart', 'geominimalist', 'HundredHearts', 'TheGreenEscape', 'AnaviaDesign', 'TwinningTemplates', 'BaileyTumblers', 'LunamCo', 'ilovelotus', 'JuliAndMila', 'RuyaTreasures', 'GiftBoxLoveCo', 'GlitterMoonshineSVG', 'MacarenaCollection', 'GreatLakesDigitals', 'NewMoonBeginnings', 'BobbisCutters', 'PlannerKate1', 'NorthPrints', 'DayBeads', 'cottonenes', 'Artiststas', 'ZECworkshop', 'theprettylittlemess', 'hooraydays', 'delezhen', 'SweetArtDesignGifts', 'LorettasBeads', 'GoldenDotLane', 'Up2ournecksinfabric', 'ThePlantGuru', 'TomorrowSeeds', 'Beatti', 'DIYPaperBoutique', 'WoodNSparksCo', 'yakutum', 'TomDesign', 'CZGrain', 'WeddingsDecorStudio', 'CreativeJamCo', 'SVGCUTTABLES', 'nicoledebruin', 'YourDIYSupply', 'SaraMarieStickers', 'HirtsGardens', 'NurseInTheMaking', 'Anniesbead', 'BudgetitDE', 'WishUponMagic', 'BigmamaDesignStudio', 'PeggySueAlso', 'MarciaEmbroidery', 'Rawkrft', 'SamiJEWELS', 'PartyGloss', 'NanasPrettyGirls', 'NisPersonalized', 'GratitudeCrystals', 'SinCityCharmz', 'GoHomeNumbers', 'PippasStudio', 'OurCaliHome', 'SweetBasilCo', 'xoFetti', 'NaturalSucculents', 'WildOakStickers', 'FabricUtopia', 'MabbRoseDesigns', 'KozeyCrafts', 'BeingHappyPrints', 'PersonalizedShed', 'EveandkUS', '2PreciousGemsImages', 'OhanaJewelsShop', 'ThePaperOutpost', 'iQuickly', 'PsychicAmandaStudio', 'azdigitaldesigns', 'icecreaMNlove', 'ShopatBash', 'ShootTheMoonGifts', 'ExpertOutfit', 'sofiamastery', 'GardenEazy', 'HouseOfGemsInc', 'Vamibo', 'MaisieMooDesign', 'HolaSunshineDesigns', 'KayleeNYC', 'ShopAfroCosmetics', 'UrbanEnV', 'FlowertownWeddings', 'CharmBarnCA', 'DynamicDimensionSVG', 'MikesCookieCutters', 'OBDesignCoByJamie', 'YolisYummiesSupplies', 'KennedyClaireCouture', 'TonyscollectionUS', 'Silveristic', 'StrawberryPartyPrint', 'ByChelseaNicole', 'MoonMountainGems', 'MlssSupplies', 'BridgeSublimation', 'JoyApparelUSA', 'MugwortAndSage', 'partiara', 'HouseOfCardsByOmen', 'CatAndBeanLtd', 'TidyLadyPrintables', 'WillowLanePaperie', 'ClipartWarehouse', 'TinySupplyShop', 'ShopTattitude', 'Nbeads', 'HoneydesignStore', 'YourlovelyshopDesign', 'EnchantedDreamerCo', 'SSweddings', 'Stickearte', 'CarleaPlans', 'FromLucyandCo', 'QualitypatchesShop', 'PEPPYBEADS', 'RaccoonDesignShop', 'meshellpnc', 'APJewelrySupplier', 'CuteLittleFabricShop', 'CatherineDesignNYC', 'SEmbroideredBoutique', 'Crystalidea', 'SugarHouseSwaddles', '13MoonsMagick', 'WimlyMugs', 'anibucco', 'BlingThatANDThat', 'ErynsHomeAndGifts', 'BM25Jewelry', 'CraftyChicksDesigns1', 'CasuallyCreativeInc', 'GlamourJewelryHouse', 'TeamHen', 'EvelynCreationsStore', 'SMNecessity', 'LoveandLuxeHandmade', 'PetalPaperCo', 'CamelliaAndLove', 'BestCelebrations', 'WeedandSeed', 'Perimade', 'MuwatiUK', 'FastCustomTees', 'PrintitoffShop', 'TopetsyCrafts', 'CustomTeaShirt', 'SassyRogueDesigns', 'thebeadchest', 'PrimroseCottages', 'BumblebeadCompany', 'SavannahandJamesCo', 'KaleidaCuts', 'Plannahannah', 'GAFTreasures', 'litkedesignsco', 'PartyPropsTreasures', 'DatShirtStudio', 'PremiumProxy4u', 'CraftyArtCafe', 'GlassWingOrganic', '28Collective', 'MaikaDaughters', 'MackandRex', 'SniggleSloth', 'ASCsupplies', 'SupplyEmporium', 'MinnieCastle', 'PastPatternsPalooza', 'wishlistplant', 'monmon85design', 'MilkMilkSugar', 'HappilyChicDesigns', 'Laceshine', 'MadeOfMetal', 'WenPearls', 'WITHPUNS', 'NewHillFarms', 'LariPrintDesign', 'ClayDoughCutters', 'LunarLandings', 'PlumHouseGallery', 'littlethings2cherish', 'SweetCartolina', 'BarkalooDesign', 'artapli', 'StudioHelloYello', 'QueenofSucculents', 'HappyGreenShopSeeds', 'CrystalBaySupplies', 'LoveLinax', 'RSVPpartydecor', 'CherCanDoIt', 'SprinkledWithPink', 'JuliesDecals', 'TumblerDesignsNMore', 'SoleiEthnic', 'ForeverWeddingCrafts', 'GuerrillaCharm', 'BlueRidgeMountainCo', 'MichelleLeeStudioGB', 'WeDoHoney', 'Gingersgreenhouse', 'WizdomStudio', 'LizzielaneBoutique', 'Rosewed', 'JADEandPAIIGE', 'Twistedpendant', 'ColourDropsUK', 'AvEwerkz', 'LovekokiGifts', 'CreateYourOwnGift', 'TheEasyDesign', 'StampByMeStudio', 'RayaBellaDesigns', 'PearlyPaperDesign', 'MinisAreUs', 'CottoDESIGN', 'WinksandTwinkles', 'uniqueandyoursgifts', 'SucculentkreationsCo', 'AllMyStarsDesigns', 'AngelesParty', 'FabricsUniverse', 'LLDgiftsByLaurenLash', 'OuferJewelry', 'EngraveMyMemories', 'DecoratedBliss', 'MsMDesignUsa', 'LuckyHeartDesignsCo', 'AvitoProducts', 'FamilyWorldShirtsUS', 'JewelVers', 'HouseOfRounds', 'happysupplies', 'MintyMarshmallows', 'CustomHappinessShop', 'VenusArtsShop', 'SunshineDaydreamerCo', 'BlueBunnyPrintables', 'LancelotDIY', 'Ottomanmarrakech', 'YouHadMeAtCrafts', 'notPERFECTLINEN', 'RoseGoldRebel', 'PickledStamps', 'KAFontDesigns', 'DesireDesignUSStore', 'DigitalLinks', 'BeadologyByHeather', 'Distinctivs', 'AnthemStickerCompany', 'hoopsbyhand', 'LDDigital', 'Rishasart', 'BusyPuzzle', 'PaveFindings4u', 'littlehappiesco', '24HourCrafts', 'JewelryBlues', 'TaricGoods', 'Framorey', 'TheStoneSanctuary', 'SBNCraftSupplies', 'Ny6designJewelry', 'EnFete', 'FabricsAndBuntings', 'CheshiresChestUK', 'AvadirAndCo', 'TarasWonderworld', 'PatternPen', 'BlushPaperieShop', 'Johnhandmadesupply', 'PerfectMatchShop', 'ConnectCo', 'nRichCollection', 'HisCorner', 'MayaPrintDesign', 'HolzteilchenDIY', 'BigHeartCutfiles', 'AmeCrystal', 'DianellaJewelryStore', 'WeddingsDecorandMore', 'GypsyyyTarot', 'BELKYmood', 'SelineLounge', 'Jasminsmagicworld', 'AnotherEast', 'fantabuloussupplies', 'RKArtPrints', 'PinkBayDesigns', 'madebynami', 'Mstudiocreationsshop', '5thstreetstudio', 'PenguinsPineapples', 'ClementinesDesignsCo', 'CaSales', 'InkandFred', 'FlashyStudioNYC', 'SVGista', 'sierrametaldesign', 'MiniatureCrush', 'Hoiaucraft', 'PrecisionMemory', 'CHIKIPUMcutfiles', 'DesigningMoments', 'PartyEight', 'SheShedCraftStore', 'SmartSeedsEmporium', 'LillysHandmades', 'thepottymouthpress', 'TheMonkeyCharmShop', 'kismetbyme', 'PinkChihuahuaFabric', 'IrisNaiderDesign', 'BBGrafix', 'MoonwakeDesignsCo', 'GemMartUSA', 'pokeyandbear', 'fromwillow', 'ViliveDE', 'BrantPointPrep', 'Party14ByBELLA', 'TheWhiteInviteGifts', 'FarmDreamArt', 'AlexKloseDesign', 'caketothetop', 'PoofThereItIsReveals', 'EveAndJoyDE', '3DWorldUS', 'LuckandLuck', 'SunnyStudioD', 'PippaPatternsCrochet', 'PersonalizedMoments1', 'DigitalPixelPH', 'themommysvg', 'PrimitiveMillworks', 'MadeInRose', 'LitzyCo', 'WolvesnWillows', 'AlwaysBlanks', 'GR8BEADS', 'ArtOfFabricFolding', 'milonic', '904Custom', 'GlassArtStories', 'erdmetaljewelry', 'NunaChula', 'piercingfashion', 'CardSharkUK', 'Grove123Designs', 'RemmDesign', 'CreatingUnkamen', 'TinTinTinFlowers', 'DavetheEagleCards', 'hellorosepaperie', 'TopWoodworksDesign', 'WishfulPaperBoutique', 'AnabellasShop', 'EmilyEstherDesigns', 'DarlingJewelryStudio', 'BrumleyandBloom', 'AllureWeddingJewelry', 'hanletteringandco', 'ViolaMirabilisDesign', 'DisynePlus', 'SvgVectorMonster', 'LittleEarsBoutique', 'RazberrySlimeCo', 'EstablishedCoGifts', 'DigiVectorArt', 'SilkPurseSowsEar', 'VikisewsPatterns', 'ShopMiniBisous', 'MonsterSVGWorld', 'EastCoastSublimation', 'BackToNatureCompany', 'PersonalizationLab', 'NecklaceDreamWorld', 'AmityBloom', 'SmallIslandSeedCo', 'CookiePrintableShop', 'zoigenesi', 'bdactivewear', 'CraftCutConcepts', 'GraphicLoveSVG', 'ClipzAndSnipz', 'themorningdoppio', 'LosAngelesParty', 'PinkMonarchPrints', 'PiercedCreations', 'LettuceBuildaHouse', 'FlowerFashionStore', 'emandsprout', 'DarethColburnDesigns', 'ShreeejiTemplate', 'KyleenDesign', 'AMJEWELRYNYC', 'NovoGraphics', 'Onlyqualityseller', 'BodyClickers', 'TheJewelryStandard', 'zoeysattic', 'VitalPiercing', 'BillyElleCo', 'AmethystGarnet', 'BeeCreativeOnline', 'CounsellorCronan', 'FreshCutsStudio', 'DahliaPaperBoutique', 'RustyCowgirlBoutique', 'giuliarehandmade', 'SVGByDesingart', 'KraftStreetPaperCo', 'OLIBLOCK', 'styledproductmockups', 'DaylilyNursery', 'PaperMinxPrintables', 'TrendyDesignsOnline', 'EarlesFolly', 'AngelStudioHD', 'heiunlimited', 'UKGIFTSTOREONLINE', 'SweetCloudDesign', 'ChicbabyStudio', 'CrocShopUK', 'wunderwunsch', 'PetiteBeads']
    try:
        for PID in list :
            response = process(driver, PID)
            print(f"Final response: {response}")
    except BaseException as err:
        print(err)
    finally:
        closeDriver(driver)
