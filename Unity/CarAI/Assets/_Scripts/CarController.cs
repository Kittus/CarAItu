using UnityEngine;
using System.Collections;
using System.Text;
using System.IO;

public class CarController : MonoBehaviour {
    StreamReader reader;
    public string fileName = "Path.txt";
    public float velocity = 4.0f;
    string line;
    Vector3 objective;
    bool moving;

    // Use this for initialization
    void Start () {
        reader = new StreamReader(fileName, Encoding.Default);
        moving = false;
    }
	
	// Update is called once per frame
	void Update () {
        if (!moving) {
            line = reader.ReadLine();

            if (line != null)
            {
                string[] entries = line.Split(' ');
                if (entries.Length == 3)
                {
                    //Debug.Log(int.Parse(entries[0]) + int.Parse(entries[1]));
                    objective = new Vector3(int.Parse(entries[0]), 0.1f, int.Parse(entries[1]));

                    var rotationVector = transform.rotation.eulerAngles;
                    rotationVector.y = - int.Parse(entries[2]) + 90;
                    transform.rotation = Quaternion.Euler(rotationVector);

                    moving = true;
                }
            }
        }

        if ((objective - gameObject.transform.position).magnitude < velocity)
        {
            gameObject.transform.position = objective;
            moving = false;
        }
        else gameObject.transform.position += (objective - gameObject.transform.position).normalized * velocity;
    }
}
