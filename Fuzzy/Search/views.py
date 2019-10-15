from . models import Dataset
from django.http import HttpResponse
# Create your views here.


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
