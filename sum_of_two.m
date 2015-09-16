function sum_of_two( info )

info = loadjson(info);
disp(info);

result.content = info.a+info.b;
result.info.short = sprintf('Matlab computed %.1f + %.1f',info.a,info.b)
outfile = [info.hash '_info.json'];


fo = fopen(outfile,'w');
fprintf(fo,savejson('',result));
fclose(fo);

