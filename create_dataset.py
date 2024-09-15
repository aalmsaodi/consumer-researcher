from langsmith import Client
from dotenv import load_dotenv
load_dotenv(override=True)
client = Client()
dataset_name = "research2"

inputs = [
    """
    PCMag has reviewed the top projectors available in 2023 to help consumers find the best options for home theater, gaming, and business presentations. Below are the top picks:

    1. **Epson Home Cinema 5050UB 4K PRO-UHD Projector**
       - **Rating:** 4.5/5
       - **Link:** [Epson Home Cinema 5050UB](https://www.pcmag.com/reviews/epson-home-cinema-5050ub-4k-pro-uhd-projector)
       - **Pros:**
         - Excellent image quality
         - HDR support
         - Flexible installation options
       - **Cons:**
         - No built-in speakers
         - Bulky design

    2. **BenQ HT2050A Home Theater Projector**
       - **Rating:** 4/5
       - **Link:** [BenQ HT2050A](https://www.pcmag.com/reviews/benq-ht2050a)
       - **Pros:**
         - Low input lag for gaming
         - Accurate color reproduction
         - Affordable price
       - **Cons:**
         - Limited zoom range
         - No lens shift

    3. **Optoma UHD50X True 4K UHD Projector**
       - **Rating:** 4/5
       - **Link:** [Optoma UHD50X](https://www.pcmag.com/reviews/optoma-uhd50x)
       - **Pros:**
         - High refresh rate for smooth motion
         - Sharp 4K image
         - Good brightness
       - **Cons:**
         - Blacks could be deeper
         - Noticeable fan noise

    *...Additional products can be included similarly...*
    """
]

outputs = [
    """
    {
      "products": [
        {
          "name": "Epson Home Cinema 5050UB 4K PRO-UHD Projector",
          "rating": "4.5/5",
          "link": "https://www.pcmag.com/reviews/epson-home-cinema-5050ub-4k-pro-uhd-projector",
          "pros": [
            "Excellent image quality",
            "HDR support",
            "Flexible installation options"
          ],
          "cons": [
            "No built-in speakers",
            "Bulky design"
          ]
        },
        {
          "name": "BenQ HT2050A Home Theater Projector",
          "rating": "4/5",
          "link": "https://www.pcmag.com/reviews/benq-ht2050a",
          "pros": [
            "Low input lag for gaming",
            "Accurate color reproduction",
            "Affordable price"
          ],
          "cons": [
            "Limited zoom range",
            "No lens shift"
          ]
        },
        {
          "name": "Optoma UHD50X True 4K UHD Projector",
          "rating": "4/5",
          "link": "https://www.pcmag.com/reviews/optoma-uhd50x",
          "pros": [
            "High refresh rate for smooth motion",
            "Sharp 4K image",
            "Good brightness"
          ],
          "cons": [
            "Blacks could be deeper",
            "Noticeable fan noise"
          ]
        }
        // ...Additional products...
      ],
      "source_quality_rating": "High",
      "source_reliability": "PCMag is a reputable and well-established source for technology reviews and product recommendations, known for thorough testing and unbiased evaluations."
    }
    """
]

# Store
dataset = client.create_dataset(
    dataset_name=dataset_name,
    description="QA pairs about DBRX model.",
)
client.create_examples(
    inputs=[{"question": q} for q in inputs],
    outputs=[{"answer": a} for a in outputs],
    dataset_id=dataset.id,
)