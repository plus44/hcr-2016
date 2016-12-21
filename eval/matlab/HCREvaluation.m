%%
%Age, Sex(0:male), BooksRead, RobotExposure, AUDIOBOOK[Info, EasytoFollow, Animacy, Likeability, Intelligence, Safety]
%%
s = [20 0 5 3 4 17 20 17 13 4 19 19 16 14 3  7 10 13 11;
    22 0 10 3 4 21 13 25 11 3 16 21 15 14 3 15 15 16 13;
    21 1 40 3 3 26 23 23  9 3 24 25 20 12 4 18 23 18 10;
    21 0  3 1 4 23 21 24 12 3 19 17 15 13 2 12 12 11 10;
    20 0 10 3 4 18 16 19  8 4 25 23 23  7 3 16 20 19  7;
    21 1 21 2 1 18 18 16  8 3 17 15 14  6 2 11 16 11  7;
    18 0 15 2 3 25 20 23 12 2 21 22 18 14 1 18 21 22 13;
    22 0 10 2 4 21 19 19 13 2 20 18 18 12 3 12 12 15 10;
    22 0 15 2 3 19 23 20 11 3 29 22 23 14 4 15 16 21 11;
    18 0  5 1 1 26 22 22 11 3 26 23 22 11 2 13 22 22 11;
    18 1  2 1 1 14 17 15 11 2 27 25 22 14 1 14 17 15 11;
    20 0  2 4 4 22 19 19 11 4 18 22 12 12 2 14 24 11 11;
    21 0  4 3 2 18 21 15  6 3 23 15 21  5 2 11 12 15  7;
    19 1 10 3 3 24 13 15 12 4 14 14 18  8 2  9 13 16  5;
   %21 0  5 3 3 19 14 18 10 4 17 14 12  7 0 15  0  0  0;
    22 0  2 3 4 12 15 15 12 4 26 22 18 12 1  8 15 13  9;
    21 0 20 1 2 19 14 15  9 4 19 20 16  9 3  9 11 12 11;
    20 0  3 3 3 15 14 17  9 2 24 23 17 12 2 11 12 12  7
    ];

sampleSize = size(s,1);
ages = s(:,1);
gender = s(:, 2);
bookRead = s(:,3);
AudioAns = s(:,5);
InterAns = s(:,10);
NInterAns = s(:,15);
AudioAnimacy = mean(s(:, 6));
AudioLikability = mean(s(:, 7));
AudioIntelligence = mean(s(:, 8));
AudioSafety = mean(s(:, 9));
InterAnimacy = mean(s(:, 11));
InterLikability = mean(s(:, 12));
InterIntelligence = mean(s(:, 13));
InterSafety = mean(s(:, 14));
NInterAnimacy = mean(s(:, 16));
NInterLikability = mean(s(:, 17));
NInterIntelligence = mean(s(:, 18));
NInterSafety = mean(s(:, 19));


males = s(s(:,2)==0, :);
MaleAudioAns = mean(males(:,5));
MaleInterAns = mean(males(:,10));
MaleNInterAns = mean(males(:,15));
audioMaleUX = sum(mean(males(:, 6:9)));
interMaleUX = sum(mean(males(:, 11:14)));
ninterMaleUX = sum(mean(males(:, 16:19)));


females = s(s(:,2)==1, :);
feMaleAudioAns = mean(females(:,5));
feMaleInterAns = mean(females(:,10));
feMaleNInterAns = mean(females(:,15));
audiofeMaleUX = sum(mean(females(:, 6:9)));
interfeMaleUX = sum(mean(females(:, 9:14)));
ninterfeMaleUX = sum(mean(females(:, 16:19)));


RExp1 = s(s(:,4)==1, :);
RExp2 = s(s(:,4)==2, :);
RExp3 = s(s(:,4)==3, :);
RExp4 = s(s(:,4)==4, :);
RExp5 = s(s(:,4)==5, :);
audioRExp1UX = sum(mean(RExp1(:, 6:9)));
audioRExp2UX = sum(mean(RExp2(:, 6:9)));
audioRExp3UX = sum(mean(RExp3(:, 6:9)));
audioRExp4UX = sum((RExp4(:, 6:9)));
audioRExp5UX = sum(mean(RExp5(:, 6:9)));
% figure
% title('Audiobook')
%bar([1 2 3 4 5],[audioRExp1UX audioRExp2UX audioRExp3UX audioRExp4UX audioRExp5UX])
interRExp1UX = sum(mean(RExp1(:, 11:14)));
interRExp2UX = sum(mean(RExp2(:, 11:14)));
interRExp3UX = sum(mean(RExp3(:, 11:14)));
interRExp4UX = sum((RExp4(:, 11:14)));
interRExp5UX = sum(mean(RExp5(:, 11:14)));
% figure
%bar([1 2 3 4 5],[interRExp1UX interRExp2UX interRExp3UX interRExp4UX interRExp5UX])
ninterRExp1UX = sum(mean(RExp1(:, 16:19)));
ninterRExp2UX = sum(mean(RExp2(:, 16:19)));
ninterRExp3UX = sum(mean(RExp3(:, 16:19)));
ninterRExp4UX = sum((RExp4(:, 16:19)));
ninterRExp5UX = sum(mean(RExp5(:, 16:19)));
% figure
%bar([1 2 3 4 5],[ninterRExp1UX ninterRExp2UX ninterRExp3UX ninterRExp4UX ninterRExp5UX])


% AudioLess = mean(AudioAns<=InterAns);
% NInterLess = mean(NInterAns<=InterAns);

fprintf('The average age is %f and the standard deviation is %f\n' , mean(ages), std(ages))
fprintf('On average %f  of the population is female\n', sum(gender)/sampleSize)
fprintf('On average, users read %f books annualy\n', mean(bookRead))
fprintf('Users scored %f on the audiobook, %f on interactive and %f on non interactive\n', mean(AudioAns)/4, mean(InterAns)/4, mean(NInterAns)/4)
fprintf('On the animacy scale we have the following data: %f for audiobook, %f for interactive and %f for non interactive\n',AudioAnimacy, InterAnimacy, NInterAnimacy);
fprintf('On the likability scale we have the following data: %f for audiobook, %f for interactive and %f for non interactive\n',AudioLikability, InterLikability, NInterLikability);
fprintf('On the percieved intelligence scale we have the following data: %f for audiobook, %f for interactive and %f for non interactive\n',AudioIntelligence, InterIntelligence, NInterIntelligence);
fprintf('On the safety scale we have the following data: %f for audiobook, %f for interactive and %f for non interactive\n',AudioSafety, InterSafety, NInterSafety);
fprintf('Males scored %f on the audiobook, %f on interactive and %f on non interactive\n', (MaleAudioAns)/4, (MaleInterAns)/4, (MaleNInterAns)/4)
fprintf('Females scored %f on the audiobook, %f on interactive and %f on non interactive\n', (feMaleAudioAns)/4, (feMaleInterAns)/4, (feMaleNInterAns)/4)
