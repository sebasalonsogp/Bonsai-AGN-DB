import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import 'react-tabs/style/react-tabs.css';

// Uses react-tabs https://www.npmjs.com/package/react-tabs

const references = [
    // {name: "name1", catalog: "catalog1", ref: "link", refLink: "https://www.google.com"},
    {catalog: "2MRS", name: "2MRS_AGN.fit", ref: "Zaw+19", refLink: "https://ui.adsabs.harvard.edu/abs/2019ApJ...872..134Z/abstract"},
    {catalog: "2QZ", name: "2QZ.fit", ref: "Croom+04", refLink: "https://ui.adsabs.harvard.edu/abs/2004ApJ...606..126C/abstract"},
    {catalog: "2SLAQ", name: "2slaqqso.fit", ref: "Croom+04", refLink: "https://ui.adsabs.harvard.edu/abs/2004MNRAS.349.1397C/abstract"},
    {catalog: "3FGL Fermi cleanups", name: "3FGL2.fits", ref: "Paiano+19", refLink: "https://ui.adsabs.harvard.edu/abs/2019ApJ...871..162P/abstract"},
    {catalog: "3LAC", name: "3LAC_highlat.fit, 3LAC_lowlat.fit, 3LAC_table7.fit", ref: "Acero+15", refLink: "https://ui.adsabs.harvard.edu/abs/2015ApJS..218...23A/abstract"},
    {catalog: "4XMM_DR10", name: "4XMM_DR10cat_v1.0.fits", ref: "Webb+20", refLink: "https://ui.adsabs.harvard.edu/abs/2020A%26A...641A.136W/abstract"},
    {catalog: "AGNELA", name: "AGNELA.tbl", ref: "Agnello+18", refLink: "https://ui.adsabs.harvard.edu/abs/2018MNRAS.475.2086A/abstract"},
    {catalog: "AKARI_J1757+5907", name: "AKARI_NED.tbl", ref: "Aoki+11", refLink: "https://ui.adsabs.harvard.edu/abs/2011PASJ...63S.457A/abstract"},
    {catalog: "ALMA_decarli", name: "alma_decarli.fits", ref: "Decarli+18", refLink: "https://ui.adsabs.harvard.edu/abs/2018ApJ...854...97D/abstract"},
    {catalog: "ATLAS", name: "ATLAS.fits", ref: "Mao+12", refLink: "https://ui.adsabs.harvard.edu/abs/2012MNRAS.426.3334M/abstract"},
    {catalog: "BAHM", name: "BAHM_NED.fits", ref: "Banerji+15", refLink: "https://ui.adsabs.harvard.edu/abs/2015MNRAS.447.3368B/abstract"},
    {catalog: "BASS", name: "BASS_agns.fit", ref: "Koss+17", refLink: "https://ui.adsabs.harvard.edu/abs/2017ApJ...850...74K/abstract"},
    {catalog: "BAT-105M", name: "BAT-105M.fits", ref: "Oh+18", refLink: "https://ui.adsabs.harvard.edu/abs/2018ApJS..235....4O/abstract"},
    {catalog: "BGGFC", name: "BGGFC_tb1.xlsx, BGGFC_tb2.xlsx", ref: "Boutsia+15", refLink: "https://ui.adsabs.harvard.edu/abs/2018ApJ...869...20B/abstract"},
    {catalog: "BQLS", name: "BQLS.tbl", ref: "More+16", refLink: "https://ui.adsabs.harvard.edu/abs/2016MNRAS.456.1595M/abstract"},
    {catalog: "BZCAT", name: "BZCAT.fit", ref: "Massaro+09", refLink: "https://ui.adsabs.harvard.edu/abs/2009A%26A...495..691M/abstract"},
    {catalog: "C-COSM", name: "C-COSM_catalog.fit", ref: "Marchesi+16", refLink: "https://ui.adsabs.harvard.edu/abs/2016ApJ...817...34M/abstract"},
    {catalog: "CDFS7", name: "CDFS7.fit", ref: "Luo+17", refLink: "https://ui.adsabs.harvard.edu/abs/2017ApJS..228....2L/abstract"},
    {catalog: "CSC2.0", name: "csc2master.fits", ref: "CSC2.0", refLink: "https://cxc.cfa.harvard.edu/csc/"},
    {catalog: "ChaMP", name: "ChaMP.tbl", ref: "Trichas+12", refLink: "https://ui.adsabs.harvard.edu/abs/2012ApJS..200...17T/abstract"},
    {catalog: "DEEP", name: "zcat.deep2.dr4_agn.fits", ref: "Newman+12", refLink: "https://ui.adsabs.harvard.edu/abs/2013ApJS..208....5N/abstract"},
    {catalog: "DR14Q", name: "DR14Q_v4_4.fits", ref: "Paris+18", refLink: "https://ui.adsabs.harvard.edu/abs/2018A%26A...613A..51P/abstract"},
    {catalog: "DR16Q", name: "DR16Q_Superset_v3.fits", ref: "Like+20", refLink: "https://ui.adsabs.harvard.edu/abs/2020ApJS..250....8L/abstract"},
    {catalog: "DUHIZ", name: "DUHIZ_tb2.fits, DUHIZ_tb3.fits", ref: "Wang+17", refLink: "https://ui.adsabs.harvard.edu/abs/2017ApJ...839...27W/abstract"},
    {catalog: "DUz6", name: "DUz6table3.fits, DUz6table6.fits", ref: "Wang+19", refLink: "https://ui.adsabs.harvard.edu/abs/2019ApJ...884...30W/abstract"},
    {catalog: "ELQS-N", name: "ELQS-S.txt", ref: "Schindler+19", refLink: "https://ui.adsabs.harvard.edu/abs/2019ApJ...871..258S/abstract"},
    {catalog: "ELQS-S", name: "ELQS-N.txt", ref: "Schindler+17", refLink: "https://ui.adsabs.harvard.edu/abs/2017ApJ...851...13S/abstract"},
    {catalog: "F2M_REDQSO", name: "F2M_REDQSO.fits", ref: "Urrutia+09", refLink: "https://ui.adsabs.harvard.edu/abs/2009ApJ...698.1095U/abstract"},
    {catalog: "FISCBA", name: "FISCBA.tbl", ref: "Fischer+98", refLink: "https://ui.adsabs.harvard.edu/abs/1998ApJ...503L.127F/abstract"},
    {catalog: "GL-DB", name: "GLDB_tbl2.fits", ref: "Ostrovski+17", refLink: "https://ui.adsabs.harvard.edu/abs/2017MNRAS.465.4325O/abstract"},
    {catalog: "GLIKMAN", name: "glikmanAGN.fits", ref: "Glikman+18", refLink: "https://ui.adsabs.harvard.edu/abs/2018ApJ...861...37G/abstract"},
    {catalog: "GaiaUnwise", name: "Gaia_unWISE_AGNs.fits", ref: "Shu+19", refLink: "https://ui.adsabs.harvard.edu/abs/2019MNRAS.489.4741S/abstract"},
    {catalog: "HAQC", name: "HAQC.fits", ref: "Heintz+16", refLink: "https://ui.adsabs.harvard.edu/abs/2016A%26A...595A..13H/abstract"},
    {catalog: "HEINTZ", name: "HEINTZ.tbl", ref: "Heintz+18", refLink: "https://ui.adsabs.harvard.edu/abs/2018A%26A...615A..43H/abstract"},
    {catalog: "HELLAS2XMM", name: "HELLAS2XMM.fit, HELLAS2XMMe.fit", ref: "Cocchia+07", refLink: "https://ui.adsabs.harvard.edu/abs/2007A%26A...466...31C/abstract"},
    {catalog: "IANTEG", name: "IANTEG_AGN.vot, simbad_agn.vot", ref: "Masetti+13", refLink: "https://ui.adsabs.harvard.edu/abs/2013A%26A...556A.120M/abstract"},
    {catalog: "IBIS", name: "IBIS.fit", ref: "Malizia+12", refLink: "https://ui.adsabs.harvard.edu/abs/2012MNRAS.426.1750M/abstract"},
    {catalog: "IKEDA", name: "IKEDA.tbl, IKEDA_tb1.xlsx, IKEDA_tb2.xlsx", ref: "Ikeda+17", refLink: "https://ui.adsabs.harvard.edu/abs/2017ApJ...846...57I/abstract"},
    {catalog: "KQCG", name: "kqcg.fit", ref: "Liao+19", refLink: "https://ui.adsabs.harvard.edu/abs/2019RAA....19...29L/abstract"},
    {catalog: "LAMDR4", name: "LAMQ4.fits", ref: "LAMOST", refLink: "http://dr4.lamost.org/doc/data-production-description"},
    {catalog: "LAMQ3", name: "LAMQ3_tb12.fit, LAMQ3_tb13.fit", ref: "Dong+18", refLink: "https://ui.adsabs.harvard.edu/abs/2018AJ....155..189D/abstract"},
    {catalog: "LIRAS", name: "LIRAS_hdet1.fit, LIRAS_hdet2.fit, LIRAS_nondet.fit", ref: "Xu+15", refLink: "https://ui.adsabs.harvard.edu/abs/2015ApJS..219...18X/abstract"},
    {catalog: "LSSA", name: "LSSA.tbl", ref: "Lucey+18", refLink: "https://ui.adsabs.harvard.edu/abs/2018MNRAS.476..927L/abstract"},
    {catalog: "LUMIz5", name: "LUMItb3.fits, LUMItb4.fits", ref: "Yang+18", refLink: "https://ui.adsabs.harvard.edu/abs/2018AJ....155..110Y/abstract"},
    {catalog: "MALS-N", name: "MALS-N.fits", ref: "Krogager+18", refLink: "https://ui.adsabs.harvard.edu/abs/2018ApJS..235...10K/abstract"},
    {catalog: "MFJC", name: "MFJC_Sample.fit, MFJC_table5.fit", ref: "McGreer+18", refLink: "https://ui.adsabs.harvard.edu/abs/2018AJ....155..131M/abstract"},
    {catalog: "MHH", name: "MHH.fit", ref: "Meusinger+11", refLink: "https://ui.adsabs.harvard.edu/abs/2011A%26A...525A..37M/abstract"},
    {catalog: "MZZ", name: "MZZ.tbl", ref: "Marano+88", refLink: "https://ui.adsabs.harvard.edu/abs/1988MNRAS.232..111M/abstract"},
    {catalog: "NBCKDE", name: "NBCKDE.fit", ref: "Richards+09", refLink: "https://ui.adsabs.harvard.edu/abs/2009ApJS..180...67R/abstract"},
    {catalog: "NBCKv3", name: "NBCKv3_cand.fit, NBCKv3_master.fit", ref: "Richards+15", refLink: "https://ui.adsabs.harvard.edu/abs/2015ApJS..219...39R/abstract"},
    {catalog: "OVRLAP", name: "OVRLAP.tbl", ref: "Jiang+15", refLink: "https://ui.adsabs.harvard.edu/abs/2015AJ....149..188J/abstract"},
    {catalog: "OzDES", name: "OzDES.fit", ref: "Tie+17", refLink: "https://ui.adsabs.harvard.edu/abs/2017AJ....153..107T/abstract"},
    {catalog: "PHILLI", name: "PHILLI.tbl", ref: "Phillips+00", refLink: "https://ui.adsabs.harvard.edu/abs/2000MNRAS.319L...7P/abstract"},
    {catalog: "PS1", name: "highzqso.fit, table9.fit", ref: "Banados+16", refLink: "https://ui.adsabs.harvard.edu/abs/2016ApJS..227...11B/abstract"},
    {catalog: "PS1MAZ", name: "PS1MAZ.tbl", ref: "Mazzucchelli+17", refLink: "https://ui.adsabs.harvard.edu/abs/2017ApJ...849...91M/abstract"},
    {catalog: "PSO", name: "PSO.tbl", ref: "Venemans+15", refLink: "https://ui.adsabs.harvard.edu/abs/2015ApJ...801L..11V/abstract"},
    {catalog: "QPQ10", name: "QPQ10.tbl", ref: "Findlay+18", refLink: "https://ui.adsabs.harvard.edu/abs/2018ApJS..236...44F/abstract"},
    {catalog: "REQ4", name: "tb2_REQ4.txt, tb3_REQ4.txt", ref: "Yang+19", refLink: "https://ui.adsabs.harvard.edu/abs/2019AJ....157..236Y/abstract"},
    {catalog: "RLQ", name: "RLQ_tb4.fit", ref: "Tuccillo+15", refLink: "https://ui.adsabs.harvard.edu/abs/2015MNRAS.449.2818T/abstract"},
    {catalog: "S82X", name: "S82X_catalog_with_photozs_unique_Xraysrcs_likely_cps_2021.fits", ref: "LaMassa+16", refLink: "https://ui.adsabs.harvard.edu/abs/2016ApJ...817..172L/abstract"},
    {catalog: "SDLENS", name: "SDLENS.tbl", ref: "Williams+18", refLink: "https://ui.adsabs.harvard.edu/abs/2018MNRAS.477L..70W/abstract"},
    {catalog: "SDSSHI", name: "SDSSHI.tbl", ref: "Jiang+16", refLink: "https://ui.adsabs.harvard.edu/abs/2016ApJ...833..222J/abstract"},
    {catalog: "SHELQS", name: "SHELQS.tbl, SHELQStbls.fits", ref: "Matsuoka+19", refLink: "https://ui.adsabs.harvard.edu/abs/2018ApJ...869..150M/abstract"},
    {catalog: "SIX", name: "SIX.fit", ref: "Bottacini+12", refLink: "https://ui.adsabs.harvard.edu/abs/2012ApJS..201...34B/abstract"},
    {catalog: "SPIDERS DR14", name: "VAC_spiders_2RXS_DR14.fits, VAC_spiders_XMMSL_DR14.fits, spiders_quasar_bhmass-DR14.fits", ref: "Coffey+19", refLink: "https://ui.adsabs.harvard.edu/abs/2019A%26A...625A.123C/abstract"},
    {catalog: "SPIN18", name: "SPIN18.tbl", ref: "Spiniello+18", refLink: "https://ui.adsabs.harvard.edu/abs/2018MNRAS.480.1163S/abstract"},
    {catalog: "SPIN19", name: "spin19_tbls.fits", ref: "Spiniello+19", refLink: "https://ui.adsabs.harvard.edu/abs/2019MNRAS.485.5086S/abstract"},
    {catalog: "SQLS", name: "SQLS_tb1.fit, SQLS_tb3.fit, SQLS_tb4.fit, SQLS_tb5.fit, SQLS_tb6.fit", ref: "Inada+12", refLink: "https://ui.adsabs.harvard.edu/abs/2012AJ....143..119I/abstract"},
    {catalog: "SQUAD", name: "DR1_quasars_master.csv", ref: "Murphy+19", refLink: "https://ui.adsabs.harvard.edu/abs/2019MNRAS.482.3458M/abstract"},
    {catalog: "SUV", name: "SUV.tbl, SUV_tbs.fits", ref: "Yang+17", refLink: "https://ui.adsabs.harvard.edu/abs/2017AJ....154..269Y/abstract"},
    {catalog: "SXDF", name: "SXDF.fits", ref: "Simpson+12", refLink: "https://ui.adsabs.harvard.edu/abs/2012MNRAS.421.3060S/abstract"},
    {catalog: "SXDS", name: "SXDS.tbl, SXDS_abc.fits", ref: "Akiyama+15", refLink: "https://ui.adsabs.harvard.edu/abs/2015PASJ...67...82A/abstract"},
    {catalog: "UFS", name: "UFS_tb1.fit, UFS_tb2.fit", ref: "Glikman+13", refLink: "https://ui.adsabs.harvard.edu/abs/2013ApJ...778..127G/abstract"},
    {catalog: "ULTRA", name: "ULTRA.tbl", ref: "Wu+15", refLink: "https://ui.adsabs.harvard.edu/abs/2015IAUGA..2251223W/abstract"},
    {catalog: "UVQS", name: "UVQS_tb4.fit", ref: "Monroe+16", refLink: "https://ui.adsabs.harvard.edu/abs/2016AJ....152...25M/abstract"},
    {catalog: "VAQL", name: "VAQL.tbl", ref: "Chehade+18", refLink: "https://ui.adsabs.harvard.edu/abs/2018MNRAS.478.1649C/abstract"},
    {catalog: "VDES2", name: "VDES2.fits", ref: "Reed+19", refLink: "https://ui.adsabs.harvard.edu/abs/2019MNRAS.487.1874R/abstract"},
    {catalog: "VIKING", name: "VIKING.tbl", ref: "Venemans+15", refLink: "https://ui.adsabs.harvard.edu/abs/2015MNRAS.453.2259V/abstract"},
    {catalog: "VIPERS", name: "VIPERS_W1_SPECTRO_PDR2.fits, VIPERS_W4_SPECTRO_PDR2.fits", ref: "Scodeggio+18", refLink: "https://ui.adsabs.harvard.edu/abs/2018A%26A...609A..84S/abstract"},
    {catalog: "VMC", name: "VMC.tbl", ref: "Ivanov+16", refLink: "https://ui.adsabs.harvard.edu/abs/2016A%26A...588A..93I/abstract"},
    {catalog: "WARSAW", name: "WARSAW.tbl", ref: "Kostrzewa-Rutkowska+18", refLink: "https://ui.adsabs.harvard.edu/abs/2018MNRAS.476..663K/abstract"},
    {catalog: "WGD", name: "WGD.fits", ref: "Agnello+18", refLink: "https://ui.adsabs.harvard.edu/abs/2018MNRAS.479.4345A/abstract"},
    {catalog: "WISEA", name: "WISEA.fit", ref: "Secrest+15", refLink: "https://ui.adsabs.harvard.edu/abs/2015ApJS..221...12S/abstract"},
    {catalog: "WISEHI", name: "WISEHI_highzqso.fit, WISEHI_tb1.fit", ref: "Wang+16", refLink: "https://ui.adsabs.harvard.edu/abs/2016ApJ...819...24W/abstract"},
    {catalog: "WOLF1", name: "WOLF1.fits", ref: "Wolf+18", refLink: "https://ui.adsabs.harvard.edu/abs/2018PASA...35...24W/abstract"},
    {catalog: "XLSS", name: "XLSS.fit", ref: "Stalin+10", refLink: "https://ui.adsabs.harvard.edu/abs/2010MNRAS.401..294S/abstract"},
    {catalog: "XMM-XXL", name: "XXL_tb2master.fit", ref: "Liu+16", refLink: "https://ui.adsabs.harvard.edu/abs/2016MNRAS.459.1602L/abstract"},
    {catalog: "XMMSMC", name: "XMMSMCtb4.fit", ref: "Maitra+19", refLink: "https://ui.adsabs.harvard.edu/abs/2016MNRAS.459.1602L/abstract"},
    {catalog: "XMSS", name: "XMSS.fit", ref: "Barcons+07", refLink: "https://ui.adsabs.harvard.edu/abs/2007A%26A...476.1191B/abstract"},
    {catalog: "XSERVS-WCDFS_ES1", name: "es1_xmm_cat.fits, wcdfs_xmm_cat.fits", ref: "Ni+21", refLink: "https://ui.adsabs.harvard.edu/abs/2021ApJS..256...21N/abstract"},
    {catalog: "XSERVS_XMMLSS", name: "XSERVS_XMMLSS.fits", ref: "Chen+18", refLink: "https://ui.adsabs.harvard.edu/abs/2018MNRAS.478.2132C/abstract"},
    {catalog: "XWAS", name: "XWAS.fit", ref: "Esquej+13", refLink: "https://ui.adsabs.harvard.edu/abs/2013A%26A...557A.123E/abstract"},
    {catalog: "YQLF", name: "YQLF.fit", ref: "Yang+18", refLink: "https://ui.adsabs.harvard.edu/abs/2018AJ....155..110Y/abstract"},
    {catalog: "eHAQ", name: "eHAQ.tbl, eHAQ_tb3.fits", ref: "Krogager+16", refLink: "https://ui.adsabs.harvard.edu/abs/2016MNRAS.455.2698K/abstract"},
    {catalog: "z6.51", name: "z6.51result.tbl", ref: "Fan+19", refLink: "https://ui.adsabs.harvard.edu/abs/2019ApJ...870L..11F/abstract"},
    {catalog: "COMP2CAT", name: "COMP2CAT.fit", ref: "Jimenez-Gallardo+19", refLink: "https://ui.adsabs.harvard.edu/abs/2019A%26A...627A.108J/abstract"},
    {catalog: "eFEDS", name: "eFEDS_AGNv17.6.fits, eROSITA_ctps.fit", ref: "eFEDS/eROSITA", refLink: "https://erosita.mpe.mpg.de/edr/eROSITAObservations/Catalogues/"},
]

const variables = [
    {name: "RA", description: "RA in degrees", hasUncertainty: false},
    {name: "DEC", description: "DEC in degrees", hasUncertainty: false},

    //_ned block
    {name: "Magnitude and Filter_ned", description: "Magnitude and Filter from ned", hasUncertainty: false},
    {name: "Photometry Points_ned", description: "Photometry Points from ned", hasUncertainty: false},

    //_simbad block
    {name: "FLUX_QUAL_U_simbad", description: "FLUX_QUAL_U from simbad", hasUncertainty: false},
    {name: "FLUX_SYSTEM_B_simbad", description: "FLUX_SYSTEM_B from simbad", hasUncertainty: false},
    {name: "FLUX_UNIT_B_simbad", description: "FLUX_UNIT_B from simbad", hasUncertainty: false},
    {name: "FLUX_SYSTEM_V_simbad", description: "FLUX_SYSTEM_V from simbad", hasUncertainty: false},
    {name: "FLUX_UNIT_V_simbad", description: "FLUX_UNIT_V from simbad", hasUncertainty: false},
    {name: "FLUX_SYSTEM_J_simbad", description: "FLUX_SYSTEM_J from simbad", hasUncertainty: false},
    {name: "FLUX_UNIT_J_simbad", description: "FLUX_UNIT_J from simbad", hasUncertainty: false},
    {name: "FLUX_SYSTEM_H_simbad", description: "FLUX_SYSTEM_H from simbad", hasUncertainty: false},
    {name: "FLUX_UNIT_H_simbad", description: "FLUX_UNIT_H from simbad", hasUncertainty: false},
    {name: "FLUX_SYSTEM_K_simbad", description: "FLUX_SYSTEM_K from simbad", hasUncertainty: false},
    {name: "FLUX_UNIT_K_simbad", description: "FLUX_UNIT_K from simbad", hasUncertainty: false},
    {name: "FLUX_SYSTEM_g_simbad", description: "FLUX_SYSTEM_g from simbad", hasUncertainty: false},
    {name: "FLUX_UNIT_g_simbad", description: "FLUX_UNIT_g from simbad", hasUncertainty: false},
    {name: "FLUX_SYSTEM_z_simbad", description: "FLUX_SYSTEM_z from simbad", hasUncertainty: false},
    {name: "FLUX_UNIT_z_simbad", description: "FLUX_UNIT_z from simbad", hasUncertainty: false},
    {name: "velocities:Value_simbad", description: "velocities:Value from simbad", hasUncertainty: false},
    {name: "velocities:me_simbad", description: "velocities:me from simbad", hasUncertainty: false},

    //_mag and _extinction block
    {name: "B_mag", description: "AB magnitude B", hasUncertainty: true},
    {name: "V_mag", description: "AB magnitude V", hasUncertainty: true},
    {name: "J_mag", description: "AB magnitude J", hasUncertainty: true},
    {name: "H_mag", description: "AB magnitude H", hasUncertainty: true},
    {name: "K_mag", description: "AB magnitude K", hasUncertainty: true},
    {name: "u_extinction", description: "extinction in the u band", hasUncertainty: false},
    {name: "g_mag", description: "AB magnitude g", hasUncertainty: true},
    {name: "g_extinction", description: "extinction in the g band", hasUncertainty: false},
    {name: "r_extinction", description: "extinction in the r band", hasUncertainty: false},
    {name: "i_extinction", description: "extinction in the i band", hasUncertainty: false},
    {name: "z_mag", description: "AB magnitude z", hasUncertainty: true},
    {name: "z_extinction", description: "extinction in the z band", hasUncertainty: false},
    {name: "Y_mag", description: "AB magnitude Y", hasUncertainty: true},
    {name: "W1_mag", description: "AB magnitude W1", hasUncertainty: true},
    {name: "W2_mag", description: "AB magnitude W2", hasUncertainty: true},
    {name: "W3_mag", description: "AB magnitude W3", hasUncertainty: true},
    {name: "W4_mag", description: "AB magnitude W4", hasUncertainty: true},
    {name: "FUV_mag", description: "AB magnitude FUV", hasUncertainty: true},
    {name: "NUV_mag", description: "AB magnitude NUV", hasUncertainty: true},

    {name: "spec_Z", description: "spectroscopic redshift", hasUncertainty: true},
    {name: "phot_Z", description: "photometric redshift", hasUncertainty: true},
    {name: "Z", description: "generic redshift, it can be either phot or spec", hasUncertainty: true},
    {name: "q_Z", description: "redshift quality flag (not yet implemented)", hasUncertainty: false},
    {name: "min_phot_Z", description: "photometric redshift lower value", hasUncertainty: false},
    {name: "max_phot_Z", description: "photometric redshift upper value", hasUncertainty: false},
    {name: "p_phot_Z", description: "photo-z quality", hasUncertainty: false},
    {name: "best_Z", description: "best redshift the order spec_z>photo_z>Z", hasUncertainty: true},
    {name: "f_best_Z", description: "flag on best redshift (not yet implemented)", hasUncertainty: false},
    //{name: "*_simbad", description: "infos from simbad"},
    //{name: "*_ned", description: "infos from ned"},
    {name: "SP_TYPE_simbad", description: "SP_TYPE from simbad", hasUncertainty: false},
    {name: "spec_class", description: "spectroscopic classification", hasUncertainty: false},
    {name: "gen_class", description: "generic classification", hasUncertainty: false},
    {name: "SED_class", description: "SED classification", hasUncertainty: false},
    {name: "spec_class", description: "spectroscopic classification", hasUncertainty: false},
    {name: "xray_class", description: "classification from xrays, extended or point-like", hasUncertainty: false},
    {name: "image_class", description: "classification based on visual examination", hasUncertainty: false},
    {name: "best_class", description: "priority classification following the above order", hasUncertainty: false},
    //{name: "*_mag", description: "AB magnitudes"},
    //{name: "xf*", description: "xray fluxes in units of erg/s/cm2"},
    //{name: "xfd*", description: "xray flux density in erg/cm2/s/Hz at 2 keV"},
    //{name: "counts*", description: "xray counts"},
    //{name: "xcr*", description: "xray count rates in cts/sec"},
    //{name: "HR*", description: "xray hardness ratio"},
    //{name: "rf*", description: "IR/radio fluxes in mJy"},
    {name: "E_B-V", description: "extinction", hasUncertainty: false},
    //{name: "snr_*", description: "signal to noise ratio"},
    //{name: "e_*", description: "e_ before a quantity is its uncertainty"},

    //NOTES on Xray bands:
    {name: "xf1", description: "0.1-2.4 keV", hasUncertainty: true},
    {name: "xf2", description: "0.2-12 keV", hasUncertainty: true},
    {name: "xf3", description: "0.2-2 keV", hasUncertainty: true},
    {name: "xf4", description: "0.5-10 keV", hasUncertainty: true},
    {name: "xf5", description: "0.5-2 keV", hasUncertainty: true},
    {name: "xf6", description: "0.5-4.5 keV", hasUncertainty: true},
    {name: "xf7", description: "0.5-7 keV", hasUncertainty: true},
    {name: "xf8", description: "BAT flux 14–195 keV", hasUncertainty: true},
    {name: "xf9", description: "2-10 keV", hasUncertainty: true},
    {name: "xf10", description: "2-12 keV", hasUncertainty: true},
    {name: "xf11", description: "2-7 keV", hasUncertainty: true},
    {name: "xf12", description: "Fermi Flux 100 MeV - 100 GeV", hasUncertainty: true},
    {name: "xf13", description: "4.5-7.5 keV", hasUncertainty: true},
    {name: "xf14", description: "0.2-0.5 keV", hasUncertainty: true},
    {name: "xf15", description: "0.5-1 keV", hasUncertainty: true},
    {name: "xf16", description: "1-2 keV", hasUncertainty: true},
    {name: "xf17", description: "2-4.5 keV", hasUncertainty: true},
    {name: "xf18", description: "4.5-12 keV", hasUncertainty: true},
    {name: "xf19", description: "Fermi Flux 1 - 100 GeV", hasUncertainty: true},
    {name: "xf20", description: "CSC m band 1.2-2.0 keV", hasUncertainty: true},
    {name: "xf21", description: "CSC s band 0.5-1.2 keV", hasUncertainty: true},
    {name: "xf22", description: "CSC u band 0.2-0.5 keV", hasUncertainty: true},
    {name: "xf23", description: "CSC w band ∼0.1-10.0 keV", hasUncertainty: true},
    {name: "xf24", description: "18-55 keV", hasUncertainty: false},
    {name: "xf25", description: "2.3-5 keV (eROSITA)", hasUncertainty: false},
    {name: "xf26", description: "0.2-5 keV (eROSITA)", hasUncertainty: false},
    //{name: "e_xcr1", description: "uncertainty of xcr1"},//e here
    //{name: "e_xfd1", description: "uncertainty of xfd1"},//e here
    {name: "counts", description: "(cts/s) follows the above numbers for the bands", hasUncertainty: true},
    {name: "xcr", description: "(cts/s) follows the above numbers for the bands", hasUncertainty: false},
    {name: "HR1", description: "from 4XMM_DR10cat_v1.0.fits", hasUncertainty: true},
    {name: "HR2", description: "from 4XMM_DR10cat_v1.0.fits", hasUncertainty: true},
    {name: "HR3", description: "from 4XMM_DR10cat_v1.0.fits", hasUncertainty: true},
    {name: "HR4", description: "from 4XMM_DR10cat_v1.0.fits", hasUncertainty: true},
    {name: "HR5", description: "HRhm from csc2master.fits", hasUncertainty: true},
    {name: "HR6", description: "HRhs from csc2master.fits", hasUncertainty: true},
    {name: "HR7", description: "HRms from csc2master.fits", hasUncertainty: true},
    {name: "HR8", description: "between 0.5-2 and 2-4.5 keV", hasUncertainty: true},
    {name: "HR9", description: "between 0.5-2 and 2-7 keV", hasUncertainty: true},
    {name: "HR10", description: "between 0.5-2 and 2-10 keV", hasUncertainty: false},

    //NOTES on radio/IR bands:
    {name: "rf1", description: "[]", hasUncertainty: false},
    {name: "rf2", description: "100 um", hasUncertainty: true},
    {name: "rf3", description: "12 um, WISE Ch3", hasUncertainty: true},
    {name: "rf4", description: "160 um", hasUncertainty: true},
    {name: "rf5", description: "20 cm", hasUncertainty: true},
    {name: "rf6", description: "21 cm/1.4 GHz", hasUncertainty: true},
    {name: "rf7", description: "24 um", hasUncertainty: true},
    {name: "rf8", description: "250 um", hasUncertainty: true},
    {name: "rf9", description: "3.4 um, WISE Ch1", hasUncertainty: true},
    {name: "rf10", description: "3.6 um, IRAC Ch1", hasUncertainty: true},
    {name: "rf11", description: "350 um", hasUncertainty: true},
    {name: "rf12", description: "4.5 um, IRAC Ch2", hasUncertainty: true},
    {name: "rf13", description: "4.6 um, WISE Ch2", hasUncertainty: true},
    {name: "rf14", description: "500 um", hasUncertainty: true},
    {name: "rf15", description: "8.0 um, IRAC Ch4", hasUncertainty: true},
    {name: "rf16", description: "5.8 um, IRAC Ch3", hasUncertainty: true},
    {name: "rf17", description: "143 GHz", hasUncertainty: false},
    {name: "rf18", description: "20 GHz", hasUncertainty: false},
    {name: "rf19", description: "8 GHz", hasUncertainty: false},
    {name: "rf20", description: "5 Ghz", hasUncertainty: false},
    {name: "rf21", description: "0.15 GHz", hasUncertainty: false},
    //{name: "e_F143", description: "uncertainty of F143"},//e here

    //snr_ block
    {name: "snr_g", description: "g signal to noise ratio", hasUncertainty: false},
    {name: "snr_i", description: "i signal to noise ratio", hasUncertainty: false},
    {name: "snr_r", description: "r signal to noise ratio", hasUncertainty: false},
    {name: "snr_u", description: "u signal to noise ratio", hasUncertainty: false},
    {name: "snr_z", description: "z signal to noise ratio", hasUncertainty: false},
    {name: "snr_W1", description: "W1 signal to noise ratio", hasUncertainty: false},
    {name: "snr_W2", description: "W2 signal to noise ratio", hasUncertainty: false},
    {name: "snr_W3", description: "W3 signal to noise ratio", hasUncertainty: false},
    {name: "snr_W4", description: "W4 signal to noise ratio", hasUncertainty: false},
]

function Information() {
    const makeReferenceTable = () => {
        return references.map((variable, index) => {
            let refColor = variable.refLink ? "blue" : "black";
            return (
                <tr key={index} className="odd:bg-white even:bg-gray-100 font-light">
                    <td className='p-2'>{variable.name}</td>
                    <td>{variable.catalog}</td>
                    <td>
                        <a 
                            target="_blank" 
                            rel="noreferrer" 
                            style={{ color: refColor }} 
                            href={variable.refLink}
                        >
                            {variable.ref}
                        </a>
                    </td>
                </tr>
            );
        });
    };

    const makeVariableTable = () => {
        return variables.map((variable, index) => {
            let uncertainty = variable.hasUncertainty ? `e_${variable.name}` : "";

            return (
                <tr key={index} className="odd:bg-white even:bg-gray-100 font-light">
                    <td className='p-2'>{variable.name}</td>
                    <td>{uncertainty}</td>
                    <td>{variable.description}</td>
                </tr>
            );
        });
    };

    return (
        <div className="px-[10%]">
            <Tabs>
                <TabList>
                    <Tab>Column Description</Tab>
                    <Tab>Table References</Tab>
                </TabList>

                <TabPanel>
                <table className='mb-20 w-full'>
                        <thead>
                            <tr className='bg-blue-600 text-left text-white'>
                                <th width="25%" className='p-2'>Column</th>
                                <th width="25%">Corresponding Uncertainty</th>
                                <th width="50%">Description</th>
                            </tr>
                        </thead>
                        <tbody>{makeVariableTable()}</tbody>
                    </table>
                </TabPanel>

                <TabPanel>
                    <table className='mb-20'>
                        <thead>
                            <tr className='bg-blue-600 text-left text-white'>
                                <th width="33%" className='p-2'>Name of the Table</th>
                                <th width="33%">Catalog</th>
                                <th width="33%">Reference</th>
                            </tr>
                        </thead>
                        <tbody>{makeReferenceTable()}</tbody>
                    </table>
                </TabPanel>
            </Tabs>
        </div>
    );
}

export default Information;