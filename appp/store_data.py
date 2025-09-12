from appp import create_app, db
from appp.data_scrape import Scrape
from appp.classdata import Database

app = create_app()

with app.app_context():
    scrape = Scrape()
    scrape.scrape_category("Builders", scrape.builder_data)
    scrape.scrape_category("NFTs, Arts, and Culture", scrape.nfts_data)
    scrape.scrape_category("Gaming", scrape.games_data)

    build_article_list = scrape.get_content(scrape.builder_data)
    gaming_article_list = scrape.get_content(scrape.games_data)
    nft_article_list = scrape.get_content(scrape.nfts_data)

    # dat = Database()
    # dat.save_paragraph("Gaming", gaming_article_list)
    # dat.save_paragraph("Builders", build_article_list)
    # dat.save_paragraph("Nfts", nft_article_list)