# Unicode tools

Search unicode character and character sequences:

* by character name
* by character code
* by unicode block

This tool depends on unicode 15.0 definition files.

* https://www.unicode.org/Public/15.0.0/ucdxml/ucd.all.flat.zip
* https://www.unicode.org/Public/emoji/15.0/emoji-sequences.txt
* https://www.unicode.org/Public/emoji/15.0/emoji-zwj-sequences.txt

## Usage

* Search by name.

```
$ ucsearch goblin
👺 1F47A JAPANESE GOBLIN
```

`ucsearch` prints character, code point or code point sequence, and name or description.
Copy characters (even if it seems garbled or character sequences!) and paste it in other intelligent tools, browsers for example, you may get the character.

* Search by code.

```
$ ucsearch --code 2200-2207
∀ 2200 FOR ALL
∁ 2201 COMPLEMENT
∂ 2202 PARTIAL DIFFERENTIAL
∃ 2203 THERE EXISTS
∄ 2204 THERE DOES NOT EXIST
∅ 2205 EMPTY SET
∆ 2206 INCREMENT
∇ 2207 NABLA
```

* Search by block.

```
$ $ ucsearch --block flag | grep -i norway
🇳🇴 1F1F3 1F1F4 flag: Norway
```

In this case, copy first two characters "🇳🇴" (\u1f1f3\u1f1f4) and paste in browser (ex. twitter's tweet textbox), you can see the national flag of Norway.

* Other options

  * `ucsearch` with ``--short`` option prints short format.

```
$ ucsearch --short --block latin
 ¡¢£¤¥¦§¨©ª«¬­®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿĀāĂăĄąĆćĈĉĊċČčĎďĐđĒēĔĕĖėĘęĚěĜĝĞğĠġĢģĤĥĦħĨĩĪīĬĭĮįİıĲĳĴĵĶķĸĹĺĻļĽľĿŀŁłŃńŅņŇňŉŊŋŌōŎŏŐőŒœŔŕŖŗŘřŚśŜŝŞşŠšŢţŤťŦŧŨũŪūŬŭŮůŰűŲųŴŵŶŷŸŹźŻżŽžſƀƁƂƃƄƅƆƇƈƉƊƋƌƍƎƏƐƑƒƓƔƕƖƗƘƙƚƛƜƝƞƟƠơƢƣƤƥƦƧƨƩƪƫƬƭƮƯưƱƲƳƴƵƶƷƸƹƺƻƼƽƾƿǀǁǂǃǄǅǆǇǈǉǊǋǌǍǎǏǐǑǒǓǔǕǖǗǘǙǚǛǜǝǞǟǠǡǢǣǤǥǦǧǨǩǪǫǬǭǮǯǰǱǲǳǴǵǶǷǸǹǺǻǼǽǾǿȀȁȂȃȄȅȆȇȈȉȊȋȌȍȎȏȐȑȒȓȔȕȖȗȘșȚțȜȝȞȟȠȡȢȣȤȥȦȧȨȩȪȫȬȭȮȯȰȱȲȳȴȵȶȷȸȹȺȻȼȽȾȿɀɁɂɃɄɅɆɇɈɉɊɋɌɍɎɏḀḁḂḃḄḅḆḇḈḉḊḋḌḍḎḏḐḑḒḓḔḕḖḗḘḙḚḛḜḝḞḟḠḡḢḣḤḥḦḧḨḩḪḫḬḭḮḯḰḱḲḳḴḵḶḷḸḹḺḻḼḽḾḿṀṁṂṃṄṅṆṇṈṉṊṋṌṍṎṏṐṑṒṓṔṕṖṗṘṙṚṛṜṝṞṟṠṡṢṣṤṥṦṧṨṩṪṫṬṭṮṯṰṱṲṳṴṵṶṷṸṹṺṻṼṽṾṿẀẁẂẃẄẅẆẇẈẉẊẋẌẍẎẏẐẑẒẓẔẕẖẗẘẙẚẛẜẝẞẟẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹỺỻỼỽỾỿⱠⱡⱢⱣⱤⱥⱦⱧⱨⱩⱪⱫⱬⱭⱮⱯⱰⱱⱲⱳⱴⱵⱶⱷⱸⱹⱺⱻⱼⱽⱾⱿ꜠꜡ꜢꜣꜤꜥꜦꜧꜨꜩꜪꜫꜬꜭꜮꜯꜰꜱꜲꜳꜴꜵꜶꜷꜸꜹꜺꜻꜼꜽꜾꜿꝀꝁꝂꝃꝄꝅꝆꝇꝈꝉꝊꝋꝌꝍꝎꝏꝐꝑꝒꝓꝔꝕꝖꝗꝘꝙꝚꝛꝜꝝꝞꝟꝠꝡꝢꝣꝤꝥꝦꝧꝨꝩꝪꝫꝬꝭꝮꝯꝰꝱꝲꝳꝴꝵꝶꝷꝸꝹꝺꝻꝼꝽꝾꝿꞀꞁꞂꞃꞄꞅꞆꞇꞈ꞉꞊ꞋꞌꞍꞎꞏꞐꞑꞒꞓꞔꞕꞖꞗꞘꞙꞚꞛꞜꞝꞞꞟꞠꞡꞢꞣꞤꞥꞦꞧꞨꞩꞪꞫꞬꞭꞮꞯꞰꞱꞲꞳꞴꞵꞶꞷꞸꞹꞺꞻꞼꞽꞾꞿꟀꟁꟂꟃꟄꟅꟆꟇꟈꟉꟊꟐꟑꟓꟕꟖꟗꟘꟙꟲꟳꟴꟵꟶꟷꟸꟹꟺꟻꟼꟽꟾꟿꬰꬱꬲꬳꬴꬵꬶꬷꬸꬹꬺꬻꬼꬽꬾꬿꭀꭁꭂꭃꭄꭅꭆꭇꭈꭉꭊꭋꭌꭍꭎꭏꭐꭑꭒꭓꭔꭕꭖꭗꭘꭙꭚ꭛ꭜꭝꭞꭟꭠꭡꭢꭣꭤꭥꭦꭧꭨꭩ꭪꭫𐞀𐞁𐞂𐞃𐞄𐞅𐞇𐞈𐞉𐞊𐞋𐞌𐞍𐞎𐞏𐞐𐞑𐞒𐞓𐞔𐞕𐞖𐞗𐞘𐞙𐞚𐞛𐞜𐞝𐞞𐞟𐞠𐞡𐞢𐞣𐞤𐞥𐞦𐞧𐞨
𐞩𐞪𐞫𐞬𐞭𐞮𐞯𐞰𐞲𐞳𐞴𐞵𐞶𐞷𐞸𐞹𐞺𝼀𝼁𝼂𝼃𝼄𝼅𝼆𝼇𝼈𝼉𝼊𝼋𝼌𝼍𝼎𝼏𝼐𝼑𝼒𝼓𝼔𝼕𝼖𝼗𝼘𝼙𝼚𝼛𝼜𝼝𝼞𝼥𝼦𝼧𝼨𝼩𝼪                                                      
```

## Install and initialize tools

Install by `pip3`.

```shell
$ pip3 install git+https://github.com/mkyutani/unicode-tools.git
```

`uccreatedatabase` command initializes unicode database.

```shell
$ uccreatedatabase
```

This command creates a file `~/.local/share/applications/unicode.db`, which is an sqlite3 file consuming about 13MB for unicode 15.0.

## Remove tools

`ucdeletedatabase` removes unicode database.

```shell
$ ucdeletedatabase
```

This command removes `~/.local/share/applications/unicode.db`.
