------------------------Labelling-----------------------------

------- Labelling Tool -------

Etiketleme yapmak için scalabel adlı algoritmayı kullanıyoruz.

~/scalabel directorysinde terminal açarak

npm run serve

komutunu çalıştırarak scalabel'i başlatıyoruz.

Google Chrome'dan http://localhost:8686/ adresine giderek, etiketleme toolu kullanılabilir.

Ayrıntılı bilgi için https://github.com/scalabel/scalabel reposu okunmalıdır


------- Toplanmış Veriler ------------

Toplanmış veriler, ubuntuda yer kalmadığından dolayı windowsun yüklü olduğu diske aktarılmıştır.

Files başlatılarak Other Locations'a tıklanır, sonrasında Windows klasörüne tıklanır. Toplanınlan veriler data klasörü içindedir.

Buradan kullanmak istediğiniz verileri ubuntuya çekerek kullanabilirsiniz. Eğer sonradan toplanılan verileri de windows dizinine aktarmak isterken, 

read-only sorunu ile karşılaşırsanız, windowsu açıp shift basılı tutarak windowsu kapatmanız gerekir.


------- Etiketlenecek verilerin hazırlanması ---------


Scalabel'da etiketleme yapabilmek için çeşitli json dosylarının hazırlanamsı gerekiyor. Scriptler PyCharm Ide'si kullanılarak venv ile hazırlanmıştır.

Bu sebeple bu scriptleri çalıştırabilmek için PyCharm'dan 'batuhan' isimli proje açılmalıdır. Hazırlanan scriptler 'scripts' dizininde bulunmaktadır. Çoğu scripti modify run config

kısmını değiştirerek kullanabilirsiniz.

Etiketleme için gerekli adımlar şu şekildedir:

1 - Öncelikle etiketlenecek image ve pointcloud dosyaları windows dizininde seçilerek ubuntu ortamına aktarılır.

2 - Scalabel etiketleme tool'u ply dosya uzantısı ile çalıştığı için pcd uzantılı dosyaların ply uzantılıya çevrilmesi gerekir. 

Bunun için pcd2ply.py scriptini kullanabilirsiniz.

Bu script input argümanı olarak pcd dosylarının olduğu pathi alır. PATH_PLY içinde belirtilen path'e ise ply dosyalarını yazar. Bu pathi kodun içinden

değiştirmelisiniz.

3- Image için json dosyası oluşturan script prepare_png_dataset_json.py.

Bu script input olarak image'ların olduğu pathi alır.

4- Pointcloud json dosyasalarını oluşturmadan önce bir ayrıntıyı anlamak gerekiyor. Platformda kullanılan lidar ve zed kamera farklı frekanslarda çalışıyor. Bu sebeple toplanılan görüntüler
senkron değildir. match_zed2_lidar.py scripti bu problemi çözmek için yazılmıştır. Image pathini ve ply pathini argüman olarak alır. matches.csv dosyası içine senkron edilmiş image ve pointcloudların isimlerini
csv dosyasına yazar.


5- Senkron edildikten sonra sırada pointcloud verilerinin json dosyasının hazırlanması kalıyor. prepare_pc_dataset_json.py scripti bu json dosyasını hazırlamak için yazılmıştır. Arguman olarak önceki scriptini çıktısı
olan matches.csv dosyasını alır.


6- Etiketlenen veri seti scalabeldan indirilebilir. Fakat çoğu algoritma polygon yerine mask kullanarak çalışıyor. Bu sebeple poly2mask.py scriptini kullanarak gereken dönüşümü yapabilirsiniz.

7- mask2poly_json scripti ile auto-label için gerekli olan json dosyası da hazırlanabilir.

---------Önemli Notlar----------

1- PARAM_DIVIDER -- Scriptlerde yer alan bu parametre, her kaç sekansta bir etiketlenecek veriyi kullanılacağını belirliyor. 3 olduğu zaman her 3 resimden birini kullanıyor.
Dilerseniz prepare_dataset.py scriptini kullanarak, kullanılacak veri setini ayrı bir klasöre alabilirsiniz. Matches.csv dosyasını arguman olarak alır.

2- ~/scalabel/local-data/items -- etikelenecek verileri koyduğumuz path.

3- Yüksek platformda kayıt edilen verilerin isimlerindeki timestamp ile alçak platformdaki farklı olmuş. Bu sebeple alçak platformda toplanan veriler için scriptlerin düzenlenmesi gerekiyor.

4- Image road etiketleme yaklaşık 15-20 saniye sürüyor.



--------------------------------- mmsegmentation -----------------------------------

Topladığımız ve etiketlediğimiz imageları, test etmek için mmsegmentation'u kullanıyoruz. Bu repoda farklı bir çok dl methodu tek repoda denenebiliyor.

Yine aynı şekilde Pycharmdan mmsegmentation adlı projeyi açarsanız, gerekli liblerin kurulu olduğu venv ile çalışabilirsiniz.

Veri seti test için kullanılan dizin mmsegmentaion/batuhan adlı dizinde bulunmaktadır. road_demo.py scripti ile veri setinin iou scorunu hesaplayabilirsiniz.

Script dizindeki imageları okuyarak pspnet50'yi kullanarak segmentation işini halleder. Daha sonra road dışındaki diğer etiketleri siler. Sonrasında bizim etiketlemiş olduğumuz gt masklerini kullanarak iou scoru hesaplar.

Showresultpyplot (51.satır) kısmını commandlinedan çıkarak segmentation kalitesine bakabilirsiniz.

mmsegmentation kendi reposunu okuyarak farklı dl methodlarını da test edebilirsiniz.


--------------------------------- mmdetection3d -------------------------------------

Bu repoda ise pointcloud object detection bulunmaktadır. Yine aynı şekilde PyCharm'dan bu projeyi açarsanız gerekli liblerin kurulduğu venv'de çalışabilirsiniz. pcd_demo.py scripti ile demoyu inceleyebilirsiniz.

