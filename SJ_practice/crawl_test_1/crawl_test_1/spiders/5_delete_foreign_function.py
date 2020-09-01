{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "kernelspec": {
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "codemirror_mode": {
        "name": "ipython",
        "version": 3
      },
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "pygments_lexer": "ipython3",
      "version": "3.7.3"
    },
    "colab": {
      "name": "delete_foreign_function.ipynb의 사본",
      "provenance": [],
      "include_colab_link": true
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/Sjing2/SJ_practice/blob/master/SJ_practice/crawl_test_1/crawl_test_1/spiders/5_delete_foreign_function.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "Sy8zqVmBrbc7",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 34
        },
        "outputId": "55432e0a-9ed1-4943-99f3-c37a4f00f754"
      },
      "source": [
        "from google.colab import drive\n",
        "drive.mount('/content/gdrive/')"
      ],
      "execution_count": 9,
      "outputs": [
        {
          "output_type": "stream",
          "text": [
            "Drive already mounted at /content/gdrive/; to attempt to forcibly remount, call drive.mount(\"/content/gdrive/\", force_remount=True).\n"
          ],
          "name": "stdout"
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "zAKSGUreh7KK",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "import re\n",
        "import pandas as pd\n",
        "import os"
      ],
      "execution_count": 10,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "nGSJ6ofqrO4q",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 35
        },
        "outputId": "f0595833-220e-4f8b-cc36-c6f7b425bf5c"
      },
      "source": [
        "%pwd"
      ],
      "execution_count": 11,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "application/vnd.google.colaboratory.intrinsic+json": {
              "type": "string"
            },
            "text/plain": [
              "'/content/gdrive/.shortcut-targets-by-id/1S7PAJP8UJtcJvFk37bryshL8PyysDzB6/인스타그램_프로파일링/Post/Region'"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 11
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "L3xl_J7lh7KO",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "os.chdir('/content/gdrive/My Drive/인스타그램_프로파일링/Post/Region')\n",
        "df = pd.read_csv('cc_region.csv')"
      ],
      "execution_count": 12,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "H7AmKexbh7KS",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 34
        },
        "outputId": "5f46fd2a-14f8-4b58-aca1-6652943bb0c2"
      },
      "source": [
        "id_lst = list(set(df['insta_id']))\n",
        "len(id_lst)"
      ],
      "execution_count": 13,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "2517"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 13
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "n0PeW8MGh7KW",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "def del_foreign(df):\n",
        "    id_lst = list(set(df['insta_id']))\n",
        "    for user_id in id_lst:\n",
        "        count = 0\n",
        "        for y in list(df[df['insta_id']==user_id]['content']):\n",
        "            if type(y) != str:\n",
        "                pass\n",
        "            elif re.search('[가-힣]', y):\n",
        "                count += 1\n",
        "        if count == 0:\n",
        "            idx = df[df['insta_id']==user_id].index\n",
        "            df.drop(idx, inplace=True)\n",
        "    return df"
      ],
      "execution_count": 14,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "Islr2axeh7KZ",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "new_df = del_foreign(df)"
      ],
      "execution_count": 15,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "yIpcA83lh7Kc",
        "colab_type": "code",
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 34
        },
        "outputId": "0e96340a-9984-4008-8030-6e103f19a35e"
      },
      "source": [
        "id_lst = list(set(new_df['insta_id']))\n",
        "len(id_lst)"
      ],
      "execution_count": 16,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "1726"
            ]
          },
          "metadata": {
            "tags": []
          },
          "execution_count": 16
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "eiRCwhVzh7Kf",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        "new_df.to_csv('/content/gdrive/My Drive/인스타그램_프로파일링/Post/cc_hangul.csv', index=False)"
      ],
      "execution_count": 17,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "rT9dIkbos7Oi",
        "colab_type": "code",
        "colab": {}
      },
      "source": [
        ""
      ],
      "execution_count": null,
      "outputs": []
    }
  ]
}