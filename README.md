# Tweet Hashtag ve Kelime Analiz Uygulaması

Bu uygulama, belirttiğiniz X (Twitter) kullanıcısının son tweetlerini tarayarak seçtiğiniz hashtag veya anahtar kelimelerin kaç farklı tweette geçtiğini gösterir.

## Kurulum

1. Bağımlılıkları yükleyin:

   ```bash
   pip install -r requirements.txt
   ```

2. Uygulamayı başlatın:

   ```bash
   flask --app app run
   ```

   veya

   ```bash
   python app.py
   ```

3. Tarayıcınızda [http://localhost:5000](http://localhost:5000) adresini açın.

## Kullanım

- Kullanıcı adını `@` işareti olmadan girin.
- Hashtag veya anahtar kelimeleri virgülle ayırarak yazın.
- Uygulama, girilen kullanıcı için en fazla 200 tweeti inceler ve her kelimenin kaç tweette geçtiğini listeler.

> **Not:** X API'sine resmi erişim olmadığı için veriler herkese açık tweetler üzerinden `snscrape` kütüphanesi ile toplanır. Kullanıcı hesabı gizliyse veya tweetler erişime kapalıysa sonuç alınamaz.
