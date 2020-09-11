# KowikiExtractor
해당 코드는 [WikiExtractor.py](http://medialab.di.unipi.it/wiki/Wikipedia_Extractor)기반으로 수정된 코드이며,
latest version의 wikiextractor와는 코드가 다릅니다. 자세한 설명은 '설명노트'를 참고해주세요.

"## 20200910 버전 ##"
-# WikiExtractor.py: xml.bz2파일을 다수 wiki text를 포함한 directory로 convert함.

-# TextCollector.py: 다수 wiki text포함 directory를 하나의 text file로 합침.

-# 해당 code는 no-doc, no-title, no-templates argument에 대한 추가 코드 수정이 완료되었음(git latest code와 다름).

-# python2.7 linux환경에서 검증됨

1. 설치

git clone ### or unzip project

2. 사용 명령어 예제

WikiExtractor.py: bzcat dataset/kowiki-20200820-pages-articles-multistream.xml.bz2| -o dataset/kowiki20200820 --processes 24 --no-doc --no-title --no-templates -

TextCollector.py: python TextCollector.py dataset/kowiki20200820 kowiki_all.txt

(사용 형태)

python3 WikiExtractor.py -o <extracted_wiki_dir> --no-templates --processes 24 --no-doc --no-title <input_file_name (kowiki-20200820-pages-articles-multistream.xml.bz2)>

python TextCollector.py <extracted_wiki_dir> <collected_file_name>


------------------------------ 이전 버전 노트 ---------------------------------------

-## 20200905 버전 ##
1. 해당 project를 서버로 옮김(python2.7 기본 인터프리터 설정)
2. 명령어 bzcat dataset/kowiki-20200820-pages-articles-multistream.xml.bz2| -o dataset/kowiki20200820 --processes 24 --no-doc --no-title --no-templates -
(Finished 7-process extraction of 0 articles in 0.0s (0.0 art/s) 에러, https://github.com/attardi/wikiextractor/issues/124)

-## 출처: http://kugancity.tistory.com/entry/%ED%95%9C%EA%B5%AD%EC%96%B4-%EB%89%B4%EC%8A%A4-%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%A1%9C-%EB%94%A5%EB%9F%AC%EB%8B%9D-%EC%8B%9C%EC%9E%91%ED%95%98%EA%B8%B0-2-%EC%9C%84%ED%82%A4-%EB%8D%A4%ED%94%84-%EB%8D%B0%EC%9D%B4%ED%84%B0-%ED%8C%8C%EC%8B%B1%ED%95%98%EA%B8%B0
1. git 윈도우 설치
2. python window내에서 사용하기: cmd에서 alias python='winpty python.exe' 출처: https://code-examples.net/ko/q/1f164d9
3. git bash에서 폴더 들어가서 python WikiExtractor.py kowiki-20180801-pages-articles-multistream.xml

-## cp949 codec 문제 in window
-## 출처: https://github.com/attardi/wikiextractor/issues/89
-## WikiExtractor.py에서 코드 변경. 밑에서 라인 2844, 2850임(2018-08-15 기준)
Solution:
According to :
https://github.com/rappdw/wikiextractor/commit/934688f8f936ffae756c7f7bd072df1df22dd554

Line 2706:
Remove:
input = fileinput.FileInput(input_file, openhook=fileinput.hook_compressed)
Add:
input = open(input_file, 'r', encoding='utf-8')

Line 2710:
Remove:
line = line.decode('utf-8')

-### 추가. template제거와 no-doc <doc~~>, no-title을 실행하도록 코드 변경한 wikiextractor.py파일은 nlpgpu4/project에 있음(이파일도 적용함)
참고링크: https://github.com/attardi/wikiextractor/pull/91/commits/e2a3b27003a1ea3d49fc9ac281c594a77175f617#diff-520f8f057b6a6cc9c94f7994130935fbR525




# WikiExtractor
[WikiExtractor.py](http://medialab.di.unipi.it/wiki/Wikipedia_Extractor) is a Python script that extracts and cleans text from a [Wikipedia database dump](http://download.wikimedia.org/).

The tool is written in Python and requires Python 2.7 or Python 3.3+ but no additional library.

For further information, see the [project Home Page](http://medialab.di.unipi.it/wiki/Wikipedia_Extractor) or the [Wiki](https://github.com/attardi/wikiextractor/wiki).

# Wikipedia Cirrus Extractor

`cirrus-extractor.py` is a version of the script that performs extraction from a Wikipedia Cirrus dump.
Cirrus dumps contain text with already expanded templates.

Cirrus dumps are available at:
[cirrussearch](http://dumps.wikimedia.org/other/cirrussearch/).

# Details

WikiExtractor performs template expansion by preprocessing the whole dump and extracting template definitions.

In order to speed up processing:

- multiprocessing is used for dealing with articles in parallel
- a cache is kept of parsed templates (only useful for repeated extractions).

## Installation

The script may be invoked directly, however it can be installed by doing:

    (sudo) python setup.py install

## Usage
The script is invoked with a Wikipedia dump file as an argument.
The output is stored in several files of similar size in a given directory.
Each file will contains several documents in this [document format](http://medialab.di.unipi.it/wiki/Document_Format).

    usage: WikiExtractor.py [-h] [-o OUTPUT] [-b n[KMG]] [-c] [--json] [--html]
                            [-l] [-s] [--lists] [-ns ns1,ns2]
                            [--templates TEMPLATES] [--no-templates] [-r]
                            [--min_text_length MIN_TEXT_LENGTH]
                            [--filter_disambig_pages] [-it abbr,b,big]
                            [-de gallery,timeline,noinclude] [--keep_tables]
                            [--processes PROCESSES] [-q] [--debug] [-a] [-v]
                            input

    Wikipedia Extractor:
    Extracts and cleans text from a Wikipedia database dump and stores output in a
    number of files of similar size in a given directory.
    Each file will contain several documents in the format:

        <doc id="" revid="" url="" title="">
            ...
            </doc>

    If the program is invoked with the --json flag, then each file will
    contain several documents formatted as json ojects, one per line, with
    the following structure

        {"id": "", "revid": "", "url":"", "title": "", "text": "..."}

    Template expansion requires preprocesssng first the whole dump and
    collecting template definitions.

    positional arguments:
      input                 XML wiki dump file

    optional arguments:
      -h, --help            show this help message and exit
      --processes PROCESSES
                            Number of processes to use (default 1)

    Output:
      -o OUTPUT, --output OUTPUT
                            directory for extracted files (or '-' for dumping to
                            stdout)
      -b n[KMG], --bytes n[KMG]
                            maximum bytes per output file (default 1M)
      -c, --compress        compress output files using bzip
      --json                write output in json format instead of the default one

    Processing:
      --html                produce HTML output, subsumes --links
      -l, --links           preserve links
      -s, --sections        preserve sections
      --lists               preserve lists
      -ns ns1,ns2, --namespaces ns1,ns2
                            accepted namespaces in links
      --templates TEMPLATES
                            use or create file containing templates
      --no-templates        Do not expand templates
      -r, --revision        Include the document revision id (default=False)
      --min_text_length MIN_TEXT_LENGTH
                            Minimum expanded text length required to write
                            document (default=0)
      --filter_disambig_pages
                            Remove pages from output that contain disabmiguation
                            markup (default=False)
      --no-doc              The output won't have the lines <doc> and </doc>
      --no-title            The output won't have the titles of the articles
      -it abbr,b,big, --ignored_tags abbr,b,big
                            comma separated list of tags that will be dropped,
                            keeping their content
      -de gallery,timeline,noinclude, --discard_elements gallery,timeline,noinclude
                            comma separated list of elements that will be removed
                            from the article text
      --keep_tables         Preserve tables in the output article text
                            (default=False)

    Special:
      -q, --quiet           suppress reporting progress info
      --debug               print debug info
      -a, --article         analyze a file containing a single article (debug
                            option)
      -v, --version         print program version


Saving templates to a file will speed up performing extraction the next time,
assuming template definitions have not changed.

Option --no-templates significantly speeds up the extractor, avoiding the cost
of expanding [MediaWiki templates](https://www.mediawiki.org/wiki/Help:Templates).

For further information, visit [the documentation](http://attardi.github.io/wikiextractor).
