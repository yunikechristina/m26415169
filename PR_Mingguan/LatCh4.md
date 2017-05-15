  363  mkdir projects; cd ~/projects; touch house{1,2,3,4,5,6,7,8,9}  nomor 1
  364  ls
  365  history

 1417  mkdir houses; cd houses; touch bungalow.txt  nomor 2
 1418  ls
 1419  cd ..
 1420  cd houses
 1421  mkdir doors; cd doors; touch bifold.txt
 1422  cd ..
 1423  mkdir outdoors
 1424  cd outdoors
 1425  mkdir vegetation; cd vegetation; touch landscape.txt
 1426  ls
 1427  history

 1429  cp {house1,house5} /houses  nomor 3
 1430  ls
 1431  cp {house1,house5} houses
 1432  ls
 1433  cd houses
 1434  ls
 1435  history

 1467  cp -ra  /usr/share/doc/initscripts* ~/projects  nomor 4
 1468  cd projects
 1469  ls
 1470  history

1472  ls | less     nomor 5
 1473  rm house{6,7,8}  nomor 6
 1474  ls
 1475  mv house{3,4} ~/projects/houses/doors   nomor 7
 1476  ls
 1477  cd houses/doors
 1478  ls
 1479  history

1480  cd
 1481  rm -rf ~/projects/houses/doors    nomor 8
 1482  ls
 1483  history

 1484  chmod 640 ~/projects/house2   nomor 9
 1485  chmod -R-w projects
 1486  chmod -R -w projects   nomor 10
 1487  ls
 1488  ls -l
 1489  history


