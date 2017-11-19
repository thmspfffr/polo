clear

cd ~/Dropbox/polo/

btc_tmp = dlmread('btc.txt');

delta_t = diff(btc_tmp(:,1));

idx = find(delta_t>180);

btc = [];

len = round(delta_t(idx)./90);

for i = 1 : length(idx)
  
  if i == 1
    btc = [btc; btc_tmp(1:idx(i),:)];
  else
    btc = [btc; btc_tmp(idx(i-1)+1:idx(i),:)];
  end
  
  btc = [btc; nan(len(i),3)];

end

btc = [btc; btc_tmp(idx(i)+1:end,:)];

btc = fixgaps(btc);

% MOVING AVERAGE

seglen = 10;

nseg = floor(length(btc)/seglen);

for iseg = 1 : nseg
  
  btc_smooth(iseg,1:3) = mean(btc((iseg-1)*seglen+1:(iseg)*seglen,1:3));
  
end


  
  
  
