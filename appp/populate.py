from appp.articlecollect import Article_collector
from appp.summarizeai import Ainteract
from appp.getnstoreq import Databaseq
from appp.conductor import Conductor
from appp import create_app,db

app= create_app()
dab = Databaseq()
art = Article_collector()
ai = Ainteract()
cd = Conductor()

with app.app_context():
    gaming_items = art.get_all_gaming_article()
    builders_items = art.get_all_builders_article()
    nfts_items = art.get_all_nfts_article()

    # gaming_summed_list = cd.sum_n_save(list_item=gaming_items, category="Gaming")
    # cd.get_n_save(summarized_list=gaming_summed_list, category="Gaming")

    # builders_summed_list = cd.sum_n_save(list_item=builders_items, category="Builders")
    # builders_summed_list=art.get_all_builder_summary()
    # cd.get_n_save(summarized_list=builders_summed_list, category="Builders")

    nfts_summed_list = cd.sum_n_save(list_item=nfts_items, category="Nfts")
    #nfts_summed_list= art.get_all_nfts_summary()
    cd.get_n_save(summarized_list=nfts_summed_list, category="Nfts")
