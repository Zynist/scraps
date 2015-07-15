import std.stdio;
import std.net.curl;

void main()
{
    string baseurl = "http://www.kakioka-jma.go.jp/cgi-bin/plot/plotNN.pl";
    string postreq = "place=kak&lang=en&datatype=provisional&datakind=e&sampling=1-min&hipasssec=150&year=2015&month=2&day=18&hour=0&min=0";

    string myurl = "http://www.kakioka-jma.go.jp/cgi-bin/plot/plotNN.pl?place=kak&lang=en&datatype=provisional&datakind=e&sampling=1-min&hipasssec=150&year=2015&month=2&day=18&hour=0&min=0";
    string content = get(myurl).idup;
    writeln(content);
}
