from django.shortcuts import render
from . forms import InputForm
from . models import Dataset
from django.http import HttpResponse
from django.db.models import Q              # Encapsulates our Query

# Create your views here.

# This function is provides an HTML based template to take input and returns the output on a HTML page as well.
# Django based UI


def search(request):
    print('Search function called.')

    # POST Requests
    if request.method == 'POST':
        print('POST')
        form = InputForm(request.POST)

        if form.is_valid():
            input_word = form.cleaned_data['Input_Word']
            print("Input Word:", input_word)

            # Querying the DB for possible matches
            results = Dataset.objects.filter(Q(word__contains=input_word))

            print("Total matches found:")
            print(results.count())
            print("-------------------")

            #           *** Algorithm/Notes ***
            #
            # 1. Select 25 (or less) words containing the input string.
            #
            # 2. Match from left | Exact Match should be the first result.
            #       - Scale = Match from (Left to Right) (100-0)
            #           Find the longest string in result.
            #       - Weight Factor = (1/3)
            #
            # 3. Count - Min/Max Value to decide the Scale (0-Min, 100- Max)
            #       - Scale = Count (High to Low) (100 - 0)
            #           Find the highest count in result.
            #       - Weight Factor = (1/3)
            #
            # 4. Short Words - Shortest/Longest length to decide the Scale(0-Longest, 100- Shortest)
            #       - Weight Factor= (1/3)
            #
            # 5. Calculate the Proportional Score
            #
            # 6. Calculate the weight as:
            #       Final Weight = sum(Score-x * Weight-x), where x in [1,2,3]

            words_weights = {}
            lengths = []
            counts = []
            match_from_left = []

            # Finding the length, count and index where the input string starts from in the results.
            for i in results:

                lengths.append(len(i.word))
                counts.append(int(i.count))
                match_from_left.append(int(i.word.find(input_word)))

            # Finding the minimum and maximum values of each of the lists to avoid redundant calculations.

            lengths_min = min(lengths)
            lengths_max = max(lengths)
            counts_min = min(counts)
            counts_max = max(counts)
            matches_min = min(match_from_left)
            matches_max = max(match_from_left)

            # Finding the Proportional Scores based on Length, Count and Index of the Input string in the word.

            for i in results:
                score_length = ((len(i.word) - lengths_max) / (lengths_min - lengths_max)) * 100
                score_count = ((int(i.count) - counts_min) / (counts_max - counts_min)) * 100
                score_match = ((int(i.word.find(input_word)) - matches_max)/(matches_min - matches_max)) * 100

                # An exact match needs to be shown as the first result, hence, overriding the final weight as 100.
                if i.word == input_word:
                    words_weights[i.word] = 100
                # Calculating other weights as per the algorithm and their values.
                else:
                    words_weights[i.word] = ((score_length*(1/3)) + (score_count*(1/3)) + (score_match*(1/3)))

            final_results = {}
            count = 0

            # Sorting the final weights in a reverse order and assigning the top 25 values to the final_results.
            for key, value in sorted(words_weights.items(), key=lambda kv: kv[1], reverse=True):
                if count < 25:
                    final_results[key] = value
                    count += 1
                else:
                    break

            # Converting the Dictionary to the JSON.
            import json

            final_results = json.dumps(final_results)
            print(final_results, type(final_results))

        return render(request, 'Output.html', {'input_word': input_word, 'results': final_results})

    # GET Requests
    else:
        form = InputForm()

    return render(request, 'Input.html', {'form': form})


# REST API which returns a JSON array of the relevant results in the desired order.


def search_service(request):
    print('Search Service called.')

    input_word = request.GET.get('q')
    # Querying the DB for possible matches
    results = Dataset.objects.filter(Q(word__contains=input_word))

    print("Total matches found:")
    print(results.count())
    print("-------------------")

    #           *** Algorithm/Notes ***
    #
    # 1. Select 25 (or less) words containing the input string.
    #
    # 2. Match from left | Exact Match should be the first result.
    #       - Scale = Match from (Left to Right) (100-0)
    #           Find the longest string in result.
    #       - Weight Factor = (1/3)
    #
    # 3. Count - Min/Max Value to decide the Scale (0-Min, 100- Max)
    #       - Scale = Count (High to Low) (100 - 0)
    #           Find the highest count in result.
    #       - Weight Factor = (1/3)
    #
    # 4. Short Words - Shortest/Longest length to decide the Scale(0-Longest, 100- Shortest)
    #       - Weight Factor= (1/3)
    #
    # 5. Calculate the Proportional Score
    #
    # 6. Calculate the weight as:
    #       Final Weight = sum(Score-x * Weight-x), where x in [1,2,3]

    words_weights = {}
    lengths = []
    counts = []
    match_from_left = []

    # Finding the length, count and index where the input string starts from in the results.
    for i in results:
        # print(i.word, " -- ", i.count, " -- ", len(i.word))

        lengths.append(len(i.word))
        counts.append(int(i.count))
        match_from_left.append(int(i.word.find(input_word)))

    # print("Lengths=", lengths)
    # print("Counts=", counts)
    # print("Match_Left", match_from_left)

    # Finding the minimum and maximum values of each of the lists to avoid redundant calculations.

    lengths_min = min(lengths)
    lengths_max = max(lengths)
    counts_min = min(counts)
    counts_max = max(counts)
    matches_min = min(match_from_left)
    matches_max = max(match_from_left)

    # Finding the Proportional Scores based on Length, Count and Index of the Input string in the word.

    for i in results:
        score_length = ((len(i.word) - lengths_max) / (lengths_min - lengths_max)) * 100
        score_count = ((int(i.count) - counts_min) / (counts_max - counts_min)) * 100
        score_match = ((int(i.word.find(input_word)) - matches_max) / (matches_min - matches_max)) * 100

        # An exact match needs to be shown as the first result, hence, overriding the final weight as 100.
        if i.word == input_word:
            words_weights[i.word] = 100
        # Calculating other weights as per the algorithm and their values.
        else:
            words_weights[i.word] = ((score_length * (1 / 3)) + (score_count * (1 / 3)) + (score_match * (1 / 3)))

    final_results = {}
    count = 0

    # Sorting the final weights in a reverse order and assigning the top 25 values to the final_results.
    for key, value in sorted(words_weights.items(), key=lambda kv: kv[1], reverse=True):
        if count < 25:
            final_results[key] = value
            count += 1
        else:
            break

    # Converting the Dictionary to the JSON.
    import json

    final_results = json.dumps(final_results)
    print(final_results, type(final_results))

    return HttpResponse(final_results, content_type='json')


def update_dataset(request):
    print('Updating the Database with Dataset')
    # Full path and name to your csv file
    csv_file_path_name = "C:\\\\Users\\\\129425\\\\Desktop\\\\Search Engine\\\\word_search.csv"

    import csv
    data_reader = csv.reader(open(csv_file_path_name), delimiter=',', quotechar='"')
    count = 0
    for row in data_reader:
        dataset = Dataset()
        dataset.word = row[0]
        dataset.count = row[1]
        dataset.save()
        count += 1
        if count % 1000 == 0:
            print(count, "records inserted.")
    print("Done")
    return HttpResponse("Updated the data.")


def delete_dataset(request):
    print("Deleting all data in the Model - Dataset.")
    # Dataset.objects.all().delete()
    print("Done!")
    return HttpResponse("Deleted the data.")
